from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import Employee, Manager, create_app, db  # noqa: E402


@pytest.fixture()
def app(tmp_path: Path):
    database_path = tmp_path / "staffly_test.db"

    flask_app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
            "SESSION_COOKIE_SECURE": False,
        }
    )

    with flask_app.app_context():
        db.drop_all()
        db.create_all()

        manager = Manager(
            full_name="Test Manager",
            restaurant_name="Test Bistro",
            email="manager@staffly.com",
        )
        manager.set_password("Staffly123!")
        db.session.add(manager)
        db.session.flush()

        employee = Employee(
            manager_id=manager.id,
            full_name="Test Employee",
            role_title="Server",
            email="employee@staffly.com",
            phone="+33 6 00 00 00 00",
            status="active",
        )
        db.session.add(employee)
        db.session.commit()

        yield flask_app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
