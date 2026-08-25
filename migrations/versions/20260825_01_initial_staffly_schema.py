"""Initial Staffly schema

Revision ID: 20260825_01
Revises:
Create Date: 2026-08-25 12:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260825_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "managers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("restaurant_name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_managers_email", "managers", ["email"], unique=False)

    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("manager_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("role_title", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("phone", sa.String(length=40), nullable=False, server_default=""),
        sa.Column(
            "status",
            sa.String(length=40),
            nullable=False,
            server_default="active",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["manager_id"], ["managers.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("manager_id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=140), nullable=False),
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
            server_default="",
        ),
        sa.Column(
            "status",
            sa.String(length=40),
            nullable=False,
            server_default="todo",
        ),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["manager_id"], ["managers.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "leave_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("manager_id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "status",
            sa.String(length=40),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["manager_id"], ["managers.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("leave_requests")
    op.drop_table("tasks")
    op.drop_table("employees")
    op.drop_index("ix_managers_email", table_name="managers")
    op.drop_table("managers")
