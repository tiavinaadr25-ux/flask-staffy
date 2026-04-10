from __future__ import annotations

import json
import os
import re
import secrets
from datetime import UTC, date, datetime
from functools import wraps
from typing import Any, Callable, TypeVar
from urllib import error as urllib_error
from urllib import request as urllib_request

import click
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
except ImportError:  # pragma: no cover - optional dependency in local dev
    MongoClient = None

    class PyMongoError(Exception):
        """Fallback error type used when pymongo is unavailable."""


load_dotenv()

db: SQLAlchemy = SQLAlchemy()
bcrypt = Bcrypt()

CSRF_SESSION_KEY = "_csrf_token"
LOGIN_SESSION_KEY = "manager_id"
DEFAULT_HUGGING_FACE_MODEL_URL = (
    "https://api-inference.huggingface.co/models/" "HuggingFaceTB/SmolLM2-1.7B-Instruct"
)
ViewFunction = TypeVar("ViewFunction", bound=Callable[..., ResponseReturnValue])


def utc_now() -> datetime:
    """Return a timezone-aware datetime for created_at fields."""
    return datetime.now(UTC)


class Manager(db.Model):
    """Represent a restaurant manager who can access the dashboard."""

    __tablename__ = "managers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    restaurant_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="manager",
        cascade="all, delete-orphan",
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="manager",
        cascade="all, delete-orphan",
    )
    leave_requests: Mapped[list["LeaveRequest"]] = relationship(
        back_populates="manager",
        cascade="all, delete-orphan",
    )

    def set_password(self, password: str) -> None:
        """Store a hashed password instead of a plain text password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Compare a candidate password with the stored hash."""
        return bool(bcrypt.check_password_hash(self.password_hash, password))


class Employee(db.Model):
    """Represent a staff member managed inside the application."""

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role_title: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), default="", nullable=False)
    phone: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )

    manager: Mapped[Manager] = relationship(back_populates="employees")
    tasks: Mapped[list["Task"]] = relationship(back_populates="employee")
    leave_requests: Mapped[list["LeaveRequest"]] = relationship(
        back_populates="employee"
    )


class Task(db.Model):
    """Represent an operational task assigned by the manager."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"), nullable=False)
    employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"))
    title: Mapped[str] = mapped_column(String(140), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="todo", nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )

    manager: Mapped[Manager] = relationship(back_populates="tasks")
    employee: Mapped[Employee | None] = relationship(back_populates="tasks")


class LeaveRequest(db.Model):
    """Represent a leave request created for a staff member."""

    __tablename__ = "leave_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )

    manager: Mapped[Manager] = relationship(back_populates="leave_requests")
    employee: Mapped[Employee] = relationship(back_populates="leave_requests")


def normalize_database_url(database_url: str) -> str:
    """Convert postgres:// URLs for SQLAlchemy compatibility."""
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql://", 1)
    return database_url


def parse_optional_date(raw_value: str) -> date | None:
    """Convert an ISO date string into a date object when present."""
    if not raw_value.strip():
        return None
    return date.fromisoformat(raw_value)


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


def get_mongo_collection(app: Flask) -> Any | None:
    """Return the MongoDB collection used for AI suggestion history."""
    mongo_uri = app.config.get("MONGO_URI", "")

    if MongoClient is None or not isinstance(mongo_uri, str) or not mongo_uri:
        return None

    mongo_client = app.extensions.get("mongo_client")
    if mongo_client is None:
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1000)
        app.extensions["mongo_client"] = mongo_client

    database_name = app.config.get("MONGO_DB_NAME", "staffly_ai")
    collection_name = app.config.get("MONGO_COLLECTION_NAME", "ai_suggestions")
    return mongo_client[database_name][collection_name]


def parse_suggestion_items(raw_text: str) -> list[str]:
    """Convert raw generated text into a clean list of suggestions."""
    normalized_lines = [line.strip(" -*0123456789.") for line in raw_text.splitlines()]
    suggestions = [line.strip() for line in normalized_lines if line.strip()]

    if suggestions:
        return suggestions[:5]

    sentence_candidates = [
        sentence.strip()
        for sentence in raw_text.replace("!", ".").split(".")
        if sentence.strip()
    ]
    return sentence_candidates[:5]


def normalize_matching_text(text: str) -> str:
    """Normalize a text so repeated phrases can be detected more reliably."""
    lowered_text = text.lower().strip()
    compact_text = re.sub(r"\s+", " ", lowered_text)
    return re.sub(r"[^\w\sàâçéèêëîïôöùûüÿœæ-]", "", compact_text)


def build_fallback_suggestions(prompt: str) -> list[str]:
    """Return action-oriented task suggestions when the AI API is unavailable."""
    normalized_prompt = normalize_matching_text(prompt)
    suggestions: list[str] = []

    def add_suggestion(item: str) -> None:
        if item not in suggestions:
            suggestions.append(item)

    if any(
        keyword in normalized_prompt
        for keyword in ("midi", "dejeuner", "déjeuner", "lunch")
    ):
        add_suggestion(
            "Lancer la mise en place et vérifier que chaque poste est"
            " prêt avant l'ouverture du midi."
        )

    if any(
        keyword in normalized_prompt
        for keyword in ("soir", "diner", "dîner", "dinner")
    ):
        add_suggestion(
            "Valider la mise en place du soir et confirmer la répartition"
            " entre la salle et la cuisine."
        )

    if "terrasse" in normalized_prompt:
        add_suggestion(
            "Préparer la terrasse et répartir les zones entre les membres de l'équipe."
        )

    if any(
        keyword in normalized_prompt
        for keyword in ("absence", "absences", "absent", "manque", "sous-effectif")
    ):
        add_suggestion(
            "Réorganiser les postes pour couvrir les absences sans ralentir le service."
        )

    if any(
        keyword in normalized_prompt
        for keyword in (
            "reservation",
            "reservations",
            "réservation",
            "réservations",
            "reservent",
            "réservent",
        )
    ):
        add_suggestion(
            "Faire un point sur les réservations et ajuster le plan de"
            " salle selon le flux attendu."
        )

    if any(
        keyword in normalized_prompt
        for keyword in ("stock", "rupture", "livraison", "produit")
    ):
        add_suggestion(
            "Contrôler les stocks critiques et signaler les manques"
            " avant le lancement du service."
        )

    add_suggestion(
        "Faire un briefing rapide avec l'équipe sur les priorités du"
        " service."
    )
    add_suggestion(
        "Vérifier la salle, le matériel et les postes de travail avant le coup de feu."
    )
    add_suggestion(
        "Suivre l'avancement des tâches critiques et réajuster la"
        " répartition si besoin."
    )

    return suggestions[:3]


def clean_generated_suggestions(
    suggestions: list[str],
    prompt: str,
    restaurant_name: str,
) -> list[str]:
    """Remove repetitive or low-value suggestions from generated content."""
    normalized_prompt = normalize_matching_text(prompt)
    normalized_restaurant = normalize_matching_text(restaurant_name)
    cleaned_suggestions: list[str] = []

    for suggestion in suggestions:
        clean_text = " ".join(suggestion.split()).strip(" -•")
        if not clean_text:
            continue

        normalized_suggestion = normalize_matching_text(clean_text)
        if normalized_prompt and normalized_prompt in normalized_suggestion:
            continue
        if normalized_restaurant and normalized_restaurant in normalized_suggestion:
            continue

        if clean_text[-1] not in ".!?":
            clean_text = f"{clean_text}."

        if clean_text not in cleaned_suggestions:
            cleaned_suggestions.append(clean_text)

    return cleaned_suggestions


def generate_ai_task_suggestions(
    app: Flask, manager: Manager, prompt: str
) -> tuple[list[str], str]:
    """Generate task suggestions with Hugging Face when configured."""
    token = app.config.get("HUGGING_FACE_API_TOKEN", "")
    model_url = app.config.get("HUGGING_FACE_MODEL_URL", "")
    fallback_suggestions = build_fallback_suggestions(prompt)

    if not isinstance(token, str) or not isinstance(model_url, str):
        return fallback_suggestions, "fallback"

    if not token or not model_url:
        return fallback_suggestions, "fallback"

    payload = {
        "inputs": (
            "Generate exactly 3 short and actionable task suggestions in"
            " French for a restaurant manager. "
            "Each suggestion must start with a verb. "
            "Do not repeat the manager request verbatim. "
            "Do not mention the restaurant name. "
            "Return only the task suggestions. "
            f"Manager request: {prompt}"
        ),
        "parameters": {
            "max_new_tokens": 120,
            "return_full_text": False,
        },
    }
    request_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    api_request = urllib_request.Request(
        model_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )

    try:
        with urllib_request.urlopen(api_request, timeout=10) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except (
        TimeoutError,
        urllib_error.URLError,
        urllib_error.HTTPError,
        json.JSONDecodeError,
    ):
        return fallback_suggestions, "fallback"

    if isinstance(response_payload, list) and response_payload:
        generated_text = str(response_payload[0].get("generated_text", "")).strip()
    elif isinstance(response_payload, dict):
        generated_text = str(response_payload.get("generated_text", "")).strip()
    else:
        generated_text = ""

    parsed_items = parse_suggestion_items(generated_text)
    cleaned_items = clean_generated_suggestions(
        parsed_items,
        prompt,
        manager.restaurant_name,
    )
    if cleaned_items:
        for fallback_suggestion in fallback_suggestions:
            if fallback_suggestion not in cleaned_items:
                cleaned_items.append(fallback_suggestion)
            if len(cleaned_items) == 3:
                break
        return cleaned_items[:3], "hugging_face"

    return fallback_suggestions, "fallback"


def save_ai_suggestion_history(
    app: Flask,
    manager: Manager,
    prompt: str,
    suggestions: list[str],
    source: str,
) -> bool:
    """Save AI suggestion history into MongoDB when available."""
    collection = get_mongo_collection(app)
    if collection is None:
        return False

    document = {
        "manager_email": manager.email,
        "manager_name": manager.full_name,
        "restaurant_name": manager.restaurant_name,
        "prompt": prompt,
        "suggestions": suggestions,
        "source": source,
        "created_at": datetime.now(UTC).isoformat(),
    }

    try:
        collection.insert_one(document)
    except PyMongoError:
        return False

    return True


def format_history_datetime(raw_value: Any) -> str:
    """Format a stored datetime value into a short French display string."""
    if isinstance(raw_value, datetime):
        parsed_datetime = raw_value.astimezone()
    else:
        raw_text = str(raw_value).strip()
        if not raw_text:
            return ""

        try:
            parsed_datetime = datetime.fromisoformat(raw_text.replace("Z", "+00:00"))
        except ValueError:
            return raw_text

    return parsed_datetime.astimezone().strftime("%d/%m/%Y à %H:%M")


def load_ai_suggestion_history(
    app: Flask,
    manager: Manager,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Load the latest AI suggestion history for the connected manager."""
    collection = get_mongo_collection(app)
    if collection is None:
        return []

    try:
        documents = (
            collection.find({"manager_email": manager.email})
            .sort(
                "created_at",
                -1,
            )
            .limit(limit)
        )
    except PyMongoError:
        return []

    history: list[dict[str, Any]] = []
    for document in documents:
        history.append(
            {
                "prompt": str(document.get("prompt", "")),
                "suggestions": list(document.get("suggestions", [])),
                "source": str(document.get("source", "fallback")),
                "created_at": format_history_datetime(
                    document.get("created_at", "")
                ),
            }
        )

    return history


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Create the Flask application used locally, in tests, and in production."""
    app = Flask(__name__)

    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "change-this-secret-before-production"),
        SQLALCHEMY_DATABASE_URI=normalize_database_url(
            os.getenv("DATABASE_URL", "sqlite:///staffly_dev.db")
        ),
        TALLY_DEMO_URL=os.getenv("TALLY_DEMO_URL", ""),
        MONGO_URI=os.getenv("MONGO_URI", os.getenv("MONGO_URL", "")),
        MONGO_DB_NAME=os.getenv("MONGO_DB_NAME", "staffly_ai"),
        MONGO_COLLECTION_NAME=os.getenv(
            "MONGO_COLLECTION_NAME",
            "ai_suggestions",
        ),
        HUGGING_FACE_API_TOKEN=os.getenv("HUGGING_FACE_API_TOKEN", ""),
        HUGGING_FACE_MODEL_URL=os.getenv(
            "HUGGING_FACE_MODEL_URL",
            DEFAULT_HUGGING_FACE_MODEL_URL,
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "0") == "1",
    )

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    bcrypt.init_app(app)

    register_template_context(app)
    register_security_headers(app)
    register_cli_commands(app)
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app


def register_template_context(app: Flask) -> None:
    """Expose reusable variables to every template."""

    @app.context_processor
    def inject_template_variables() -> dict[str, Any]:
        return {
            "csrf_token": get_or_create_csrf_token(),
            "current_manager": get_current_manager(),
            "tally_demo_url": app.config.get("TALLY_DEMO_URL", ""),
        }


def register_security_headers(app: Flask) -> None:
    """Attach a few lightweight security headers to the responses."""

    @app.after_request
    def add_security_headers(response: Any) -> Any:
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


def register_cli_commands(app: Flask) -> None:
    """Register helper commands for local project setup."""

    @app.cli.command("init-db")
    def init_db_command() -> None:
        """Create database tables locally."""
        with app.app_context():
            db.drop_all()
            db.create_all()
        click.echo("Database tables created.")

    @app.cli.command("seed-demo-data")
    def seed_demo_data_command() -> None:
        """Create a demo manager and sample records for presentations."""
        with app.app_context():
            existing_manager = db.session.scalar(
                select(Manager).where(Manager.email == "manager@staffly.com")
            )

            if existing_manager is not None:
                click.echo("Demo data already exists.")
                return

            manager = Manager(
                full_name="Tia Manager",
                restaurant_name="Staffly Bistro",
                email="manager@staffly.com",
            )
            manager.set_password("Staffly123!")
            db.session.add(manager)
            db.session.flush()

            employee_one = Employee(
                manager_id=manager.id,
                full_name="Aina Rakoto",
                role_title="Chef de rang",
                email="aina@staffly.com",
                phone="+33 6 11 22 33 44",
            )
            employee_two = Employee(
                manager_id=manager.id,
                full_name="Mickael Rabe",
                role_title="Commis de cuisine",
                email="mickael@staffly.com",
                phone="+33 6 55 44 33 22",
            )
            db.session.add_all([employee_one, employee_two])
            db.session.flush()

            task = Task(
                manager_id=manager.id,
                employee_id=employee_one.id,
                title="Prepare the lunch service checklist",
                description="Check tables, booking notes, and stock for lunch.",
                status="in_progress",
                due_date=date.today(),
            )
            leave_request = LeaveRequest(
                manager_id=manager.id,
                employee_id=employee_two.id,
                start_date=date.today(),
                end_date=date.today(),
                reason="Medical appointment",
                status="pending",
            )

            db.session.add_all([task, leave_request])
            db.session.commit()

        click.echo("Demo data created.")


def register_routes(app: Flask) -> None:
    """Register the routes used by the Staffly MVP."""

    def render_tasks_page(
        manager: Manager,
        *,
        prompt: str = "",
        suggestions: list[str] | None = None,
        generation_source: str = "",
        status_code: int = 200,
    ) -> ResponseReturnValue:
        """Render the task page with the task list and AI suggestion widgets."""
        task_list = db.session.scalars(
            select(Task)
            .where(Task.manager_id == manager.id)
            .order_by(Task.created_at.desc())
        ).all()

        return (
            render_template(
                "tasks.html",
                tasks=task_list,
                prompt=prompt,
                suggestions=suggestions or [],
                generation_source=generation_source,
            ),
            status_code,
        )

    @app.route("/")
    def home() -> ResponseReturnValue:
        manager_count = (
            db.session.scalar(select(func.count()).select_from(Manager)) or 0
        )
        employee_count = (
            db.session.scalar(select(func.count()).select_from(Employee)) or 0
        )
        task_count = db.session.scalar(select(func.count()).select_from(Task)) or 0
        return render_template(
            "home.html",
            manager_count=manager_count,
            employee_count=employee_count,
            task_count=task_count,
        )

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

            existing_manager = db.session.scalar(
                select(Manager).where(Manager.email == email)
            )
            if existing_manager is not None:
                flash("An account already exists with this email.", "error")
                return render_template("register.html"), 409

            manager = Manager(
                full_name=full_name,
                restaurant_name=restaurant_name,
                email=email,
            )
            manager.set_password(password)
            db.session.add(manager)
            db.session.commit()

            session.clear()
            session[LOGIN_SESSION_KEY] = manager.id
            session[CSRF_SESSION_KEY] = secrets.token_hex(16)
            flash("Your Staffly account is ready.", "success")
            return redirect(url_for("dashboard"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login() -> ResponseReturnValue:
        if request.method == "POST":
            validate_csrf_token(request.form.get("csrf_token"))

            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            manager = db.session.scalar(select(Manager).where(Manager.email == email))

            if manager is None or not manager.check_password(password):
                flash("Invalid email or password.", "error")
                return render_template("login.html"), 401

            session.clear()
            session[LOGIN_SESSION_KEY] = manager.id
            session[CSRF_SESSION_KEY] = secrets.token_hex(16)
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

        tasks = db.session.scalars(
            select(Task)
            .where(Task.manager_id == manager.id)
            .order_by(Task.created_at.desc())
            .limit(5)
        ).all()

        return render_template(
            "dashboard.html",
            manager=manager,
            task_count=len(manager.tasks),
            is_workspace_empty=len(manager.tasks) == 0,
            tasks=tasks,
        )

    @app.route("/employees")
    @login_required
    def employees() -> ResponseReturnValue:
        manager = get_current_manager()
        assert manager is not None

        employee_list = db.session.scalars(
            select(Employee)
            .where(Employee.manager_id == manager.id)
            .order_by(Employee.full_name.asc())
        ).all()
        return render_template("employees.html", employees=employee_list)

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
                return (
                    render_template(
                        "task_form.html",
                        task=None,
                    ),
                    400,
                )

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
                return (
                    render_template(
                        "task_form.html",
                        task=task,
                    ),
                    400,
                )

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

        leave_request_list = db.session.scalars(
            select(LeaveRequest)
            .where(LeaveRequest.manager_id == manager.id)
            .order_by(LeaveRequest.created_at.desc())
        ).all()
        return render_template(
            "leave_requests.html",
            leave_requests=leave_request_list,
        )

    @app.route("/leave-requests/new", methods=["GET", "POST"])
    @login_required
    def leave_request_create() -> ResponseReturnValue:
        manager = get_current_manager()
        assert manager is not None

        employee_list = db.session.scalars(
            select(Employee)
            .where(Employee.manager_id == manager.id)
            .order_by(Employee.full_name.asc())
        ).all()

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


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
