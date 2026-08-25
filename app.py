from __future__ import annotations

from staffly import create_app
from staffly.extensions import bcrypt, db
from staffly.models import Employee, LeaveRequest, Manager, Task

app = create_app()

__all__ = [
    "Employee",
    "LeaveRequest",
    "Manager",
    "Task",
    "app",
    "bcrypt",
    "create_app",
    "db",
]


if __name__ == "__main__":
    app.run(debug=True)
