from __future__ import annotations

from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from flask import Flask

from .cli import register_cli_commands
from .config import configure_app
from .extensions import bcrypt, db
from .routes import register_routes
from .security import (
    get_current_manager,
    get_or_create_csrf_token,
    register_security_headers,
)


def register_template_context(app: Flask) -> None:
    """Expose reusable variables to every template."""

    @app.context_processor
    def inject_template_variables() -> dict[str, Any]:
        return {
            "csrf_token": get_or_create_csrf_token(),
            "current_manager": get_current_manager(),
            "tally_demo_url": app.config.get("TALLY_DEMO_URL", ""),
        }


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Create the Flask application used locally, in tests, and in production."""
    load_dotenv()

    project_root = Path(__file__).resolve().parents[1]
    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )
    configure_app(app, test_config)

    db.init_app(app)
    bcrypt.init_app(app)

    register_template_context(app)
    register_security_headers(app)
    register_cli_commands(app)
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app
