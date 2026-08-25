from __future__ import annotations

from datetime import date

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask import url_for
from flask.typing import ResponseReturnValue

from .extensions import db
from .models import Employee, LeaveRequest, Manager, Task
from .repositories import (
    count_rows,
    get_manager_by_email,
    list_employees_for_manager,
    list_leave_requests_for_manager,
    list_recent_tasks_for_manager,
)
from .security import (
    get_current_manager,
    get_owned_employee_or_404,
    get_owned_leave_request_or_404,
    get_owned_task_or_404,
    login_required,
    start_manager_session,
    validate_csrf_token,
)
from .services import (
    authenticate_manager,
    create_manager_account,
    generate_ai_task_suggestions,
    parse_optional_date,
    save_ai_suggestion_history,
)


def register_routes(app: Flask) -> None:
    """Register the routes used by the Staffly application."""

    def render_tasks_page(
        manager: Manager,
        *,
        prompt: str = "",
        suggestions: list[str] | None = None,
        generation_source: str = "",
        status_code: int = 200,
    ) -> ResponseReturnValue:
        """Render the task page with the task list and AI suggestion widgets."""
        return (
            render_template(
                "tasks.html",
                tasks=list_recent_tasks_for_manager(manager.id),
                prompt=prompt,
                suggestions=suggestions or [],
                generation_source=generation_source,
            ),
            status_code,
        )

    @app.route("/")
    def home() -> ResponseReturnValue:
        return render_template(
            "home.html",
            manager_count=count_rows(Manager),
            employee_count=count_rows(Employee),
            task_count=count_rows(Task),
        )

    @app.get("/health")
    def health() -> ResponseReturnValue:
        """Expose a lightweight health endpoint for ops and deployments."""
        return jsonify({"status": "ok", "application": "staffly"}), 200

    @app.route("/register", methods=["GET", "POST"])
    @app.route("/inscription", methods=["GET", "POST"])
    def register() -> ResponseReturnValue:
        if get_current_manager() is not None:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            validate_csrf_token(request.form.get("csrf_token"))

            full_name = request.form.get("full_name", "").strip()
            restaurant_name = request.form.get("restaurant_name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            password_confirmation = request.form.get("password_confirmation", "")

            if not full_name or not restaurant_name or not email or not password:
                flash("Please complete all required fields.", "error")
                return render_template("register.html"), 400

            if len(password) < 8:
                flash("Your password must contain at least 8 characters.", "error")
                return render_template("register.html"), 400

            if password != password_confirmation:
                flash("Passwords do not match.", "error")
                return render_template("register.html"), 400

            if get_manager_by_email(email) is not None:
                flash("An account already exists with this email.", "error")
                return render_template("register.html"), 409

            manager = create_manager_account(
                full_name=full_name,
                restaurant_name=restaurant_name,
                email=email,
                password=password,
            )
            start_manager_session(manager.id)
            flash("Your Staffly account is ready.", "success")
            return redirect(url_for("dashboard"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login() -> ResponseReturnValue:
        if request.method == "POST":
            validate_csrf_token(request.form.get("csrf_token"))

            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            manager = authenticate_manager(email, password)

            if manager is None:
                flash("Invalid email or password.", "error")
                return render_template("login.html"), 401

            start_manager_session(manager.id)
            flash("Welcome back.", "success")
            return redirect(url_for("dashboard"))

        if get_current_manager() is not None:
            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route("/connexion", methods=["POST"])
    def legacy_login() -> ResponseReturnValue:
        """Keep the old route working while the project evolves."""
        return login()

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout() -> ResponseReturnValue:
        validate_csrf_token(request.form.get("csrf_token"))
        session.clear()
        flash("You have been signed out.", "success")
        return redirect(url_for("login"))

    @app.route("/dashboard")
    @login_required
    def dashboard() -> ResponseReturnValue:
        manager = get_current_manager()
        assert manager is not None

        return render_template(
            "dashboard.html",
            manager=manager,
            task_count=len(manager.tasks),
            is_workspace_empty=len(manager.tasks) == 0,
            tasks=list_recent_tasks_for_manager(manager.id, limit=5),
        )

    @app.route("/employees")
    @login_required
    def employees() -> ResponseReturnValue:
        manager = get_current_manager()
        assert manager is not None
        return render_template(
            "employees.html",
            employees=list_employees_for_manager(manager.id),
        )

    @app.route("/employees/new", methods=["GET", "POST"])
    @login_required
    def employee_create() -> ResponseReturnValue:
        manager = get_current_manager()
        assert manager is not None

        if request.method == "POST":
            validate_csrf_token(request.form.get("csrf_token"))

            full_name = request.form.get("full_name", "").strip()
            role_title = request.form.get("role_title", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            status = request.form.get("status", "active").strip() or "active"

            if not full_name or not role_title:
                flash("Full name and role are required.", "error")
                return render_template("employee_form.html", employee=None), 400

            employee = Employee(
                manager_id=manager.id,
                full_name=full_name,
                role_title=role_title,
                email=email,
                phone=phone,
                status=status,
            )
            db.session.add(employee)
            db.session.commit()
            flash("Employee created successfully.", "success")
            return redirect(url_for("employees"))

        return render_template("employee_form.html", employee=None)

    @app.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
    @login_required
    def employee_edit(employee_id: int) -> ResponseReturnValue:
        employee = get_owned_employee_or_404(employee_id)

        if request.method == "POST":
            validate_csrf_token(request.form.get("csrf_token"))

            employee.full_name = request.form.get("full_name", "").strip()
            employee.role_title = request.form.get("role_title", "").strip()
            employee.email = request.form.get("email", "").strip()
            employee.phone = request.form.get("phone", "").strip()
            employee.status = request.form.get("status", "active").strip() or "active"

            if not employee.full_name or not employee.role_title:
                flash("Full name and role are required.", "error")
                return render_template("employee_form.html", employee=employee), 400

            db.session.commit()
            flash("Employee updated successfully.", "success")
            return redirect(url_for("employees"))

        return render_template("employee_form.html", employee=employee)

    @app.route("/employees/<int:employee_id>/delete", methods=["POST"])
    @login_required
    def employee_delete(employee_id: int) -> ResponseReturnValue:
        validate_csrf_token(request.form.get("csrf_token"))
        employee = get_owned_employee_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        flash("Employee deleted.", "success")
        return redirect(url_for("employees"))

    @app.route("/tasks", methods=["GET", "POST"])
    @login_required
    def tasks() -> ResponseReturnValue:
        manager = get_current_manager()
        assert manager is not None

        if request.method == "POST":
            validate_csrf_token(request.form.get("csrf_token"))
            prompt = request.form.get("prompt", "").strip()

            if not prompt:
                flash("Please describe the shift or context first.", "error")
                return render_tasks_page(manager, prompt=prompt, status_code=400)

            suggestions, generation_source = generate_ai_task_suggestions(
                app,
                manager,
                prompt,
            )
            history_saved = save_ai_suggestion_history(
                app,
                manager,
                prompt,
                suggestions,
                generation_source,
            )

            if history_saved:
                flash("AI suggestions generated and saved.", "success")
            else:
                flash("AI suggestions generated.", "success")

            return render_tasks_page(
                manager,
                prompt=prompt,
                suggestions=suggestions,
                generation_source=generation_source,
            )

        return render_tasks_page(manager)

    @app.route("/tasks/new", methods=["GET", "POST"])
    @login_required
    def task_create() -> ResponseReturnValue:
        manager = get_current_manager()
        assert manager is not None

        if request.method == "POST":
            validate_csrf_token(request.form.get("csrf_token"))

            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            status = request.form.get("status", "todo").strip() or "todo"
            due_date_raw = request.form.get("due_date", "").strip()

            if not title:
                flash("Task title is required.", "error")
                return render_template("task_form.html", task=None), 400

            task = Task(
                manager_id=manager.id,
                title=title,
                description=description,
                status=status,
                due_date=parse_optional_date(due_date_raw),
            )
            db.session.add(task)
            db.session.commit()
            flash("Task created successfully.", "success")
            return redirect(url_for("tasks"))

        return render_template("task_form.html", task=None)

    @app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
    @login_required
    def task_edit(task_id: int) -> ResponseReturnValue:
        task = get_owned_task_or_404(task_id)

        if request.method == "POST":
            validate_csrf_token(request.form.get("csrf_token"))

            task.title = request.form.get("title", "").strip()
            task.description = request.form.get("description", "").strip()
            task.status = request.form.get("status", "todo").strip() or "todo"
            task.due_date = parse_optional_date(
                request.form.get("due_date", "").strip()
            )

            if not task.title:
                flash("Task title is required.", "error")
                return render_template("task_form.html", task=task), 400

            db.session.commit()
            flash("Task updated successfully.", "success")
            return redirect(url_for("tasks"))

        return render_template("task_form.html", task=task)

    @app.route("/tasks/<int:task_id>/delete", methods=["POST"])
    @login_required
    def task_delete(task_id: int) -> ResponseReturnValue:
        validate_csrf_token(request.form.get("csrf_token"))
        task = get_owned_task_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted.", "success")
        return redirect(url_for("tasks"))

    @app.route("/leave-requests")
    @login_required
    def leave_requests() -> ResponseReturnValue:
        manager = get_current_manager()
        assert manager is not None

        return render_template(
            "leave_requests.html",
            leave_requests=list_leave_requests_for_manager(manager.id),
        )

    @app.route("/leave-requests/new", methods=["GET", "POST"])
    @login_required
    def leave_request_create() -> ResponseReturnValue:
        manager = get_current_manager()
        assert manager is not None

        employee_list = list_employees_for_manager(manager.id)

        if request.method == "POST":
            validate_csrf_token(request.form.get("csrf_token"))

            employee_id_raw = request.form.get("employee_id", "").strip()
            start_date_raw = request.form.get("start_date", "").strip()
            end_date_raw = request.form.get("end_date", "").strip()
            reason = request.form.get("reason", "").strip()

            if not employee_id_raw or not start_date_raw or not end_date_raw:
                flash("Employee, start date, and end date are required.", "error")
                return (
                    render_template(
                        "leave_request_form.html",
                        employees=employee_list,
                    ),
                    400,
                )

            employee = get_owned_employee_or_404(int(employee_id_raw))
            leave_request = LeaveRequest(
                manager_id=manager.id,
                employee_id=employee.id,
                start_date=date.fromisoformat(start_date_raw),
                end_date=date.fromisoformat(end_date_raw),
                reason=reason,
                status="pending",
            )
            db.session.add(leave_request)
            db.session.commit()
            flash("Leave request created successfully.", "success")
            return redirect(url_for("leave_requests"))

        return render_template("leave_request_form.html", employees=employee_list)

    @app.route("/leave-requests/<int:leave_request_id>/status", methods=["POST"])
    @login_required
    def leave_request_status(leave_request_id: int) -> ResponseReturnValue:
        validate_csrf_token(request.form.get("csrf_token"))
        leave_request = get_owned_leave_request_or_404(leave_request_id)
        next_status = request.form.get("status", "pending").strip()

        if next_status not in {"pending", "approved", "rejected"}:
            flash("Invalid status.", "error")
            return redirect(url_for("leave_requests"))

        leave_request.status = next_status
        db.session.commit()
        flash("Leave request status updated.", "success")
        return redirect(url_for("leave_requests"))
