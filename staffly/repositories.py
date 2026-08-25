from __future__ import annotations

from typing import TypeVar

from sqlalchemy import func, select

from .extensions import db
from .models import Employee, LeaveRequest, Manager, Task

ModelType = TypeVar("ModelType", Manager, Employee, Task, LeaveRequest)


def count_rows(model: type[ModelType]) -> int:
    """Return the number of rows for a given SQLAlchemy model."""
    return db.session.scalar(select(func.count()).select_from(model)) or 0


def get_manager_by_email(email: str) -> Manager | None:
    """Load a manager by email."""
    return db.session.scalar(select(Manager).where(Manager.email == email))


def list_recent_tasks_for_manager(
    manager_id: int,
    limit: int | None = None,
) -> list[Task]:
    """Return a manager task list sorted from newest to oldest."""
    query = (
        select(Task)
        .where(Task.manager_id == manager_id)
        .order_by(Task.created_at.desc())
    )
    if limit is not None:
        query = query.limit(limit)
    return list(db.session.scalars(query).all())


def list_employees_for_manager(manager_id: int) -> list[Employee]:
    """Return employees sorted alphabetically for a given manager."""
    query = (
        select(Employee)
        .where(Employee.manager_id == manager_id)
        .order_by(Employee.full_name.asc())
    )
    return list(db.session.scalars(query).all())


def list_leave_requests_for_manager(
    manager_id: int,
    limit: int | None = None,
) -> list[LeaveRequest]:
    """Return leave requests sorted from newest to oldest."""
    query = (
        select(LeaveRequest)
        .where(LeaveRequest.manager_id == manager_id)
        .order_by(LeaveRequest.created_at.desc())
    )
    if limit is not None:
        query = query.limit(limit)
    return list(db.session.scalars(query).all())
