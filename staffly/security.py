from __future__ import annotations

import secrets
from functools import wraps
from typing import Any, Callable, TypeVar

from flask import abort, flash, redirect, session, url_for
from flask.typing import ResponseReturnValue

from .extensions import db
from .models import Employee, LeaveRequest, Manager, Task

CSRF_SESSION_KEY = "_csrf_token"
LOGIN_SESSION_KEY = "manager_id"
ViewFunction = TypeVar("ViewFunction", bound=Callable[..., ResponseReturnValue])


def get_or_create_csrf_token() -> str:
    """Create one CSRF token per session and reuse it for forms."""
    csrf_token = session.get(CSRF_SESSION_KEY)
    if isinstance(csrf_token, str):
        return csrf_token

    csrf_token = secrets.token_hex(16)
    session[CSRF_SESSION_KEY] = csrf_token
    return csrf_token


def validate_csrf_token(submitted_token: str | None) -> None:
    """Reject requests with a missing or invalid CSRF token."""
    expected_token = session.get(CSRF_SESSION_KEY)

    if not isinstance(expected_token, str) or not isinstance(submitted_token, str):
        abort(400, "Missing security token.")

    if not secrets.compare_digest(expected_token, submitted_token):
        abort(400, "Invalid security token.")


def start_manager_session(manager_id: int) -> None:
    """Refresh the authenticated session for the connected manager."""
    session.clear()
    session[LOGIN_SESSION_KEY] = manager_id
    session[CSRF_SESSION_KEY] = secrets.token_hex(16)


def get_current_manager() -> Manager | None:
    """Return the connected manager based on the session."""
    manager_id = session.get(LOGIN_SESSION_KEY)
    if not isinstance(manager_id, int):
        return None
    return db.session.get(Manager, manager_id)


def login_required(view_function: ViewFunction) -> ViewFunction:
    """Protect routes that require a connected manager."""

    @wraps(view_function)
    def wrapped_view(*args: Any, **kwargs: Any) -> ResponseReturnValue:
        if get_current_manager() is None:
            flash("Please sign in to access this page.", "error")
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)

    return wrapped_view  # type: ignore[return-value]


def get_owned_employee_or_404(employee_id: int) -> Employee:
    """Load an employee and ensure it belongs to the connected manager."""
    manager = get_current_manager()
    employee = db.session.get(Employee, employee_id)

    if manager is None or employee is None or employee.manager_id != manager.id:
        abort(404)

    return employee


def get_owned_task_or_404(task_id: int) -> Task:
    """Load a task and ensure it belongs to the connected manager."""
    manager = get_current_manager()
    task = db.session.get(Task, task_id)

    if manager is None or task is None or task.manager_id != manager.id:
        abort(404)

    return task


def get_owned_leave_request_or_404(leave_request_id: int) -> LeaveRequest:
    """Load a leave request and ensure it belongs to the connected manager."""
    manager = get_current_manager()
    leave_request = db.session.get(LeaveRequest, leave_request_id)

    if (
        manager is None
        or leave_request is None
        or leave_request.manager_id != manager.id
    ):
        abort(404)

    return leave_request


def register_security_headers(app: Any) -> None:
    """Attach lightweight security headers to every response."""

    @app.after_request
    def add_security_headers(response: Any) -> Any:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "connect-src 'self' https://api-inference.huggingface.co; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        return response
