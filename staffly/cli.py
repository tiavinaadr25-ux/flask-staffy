from __future__ import annotations

import click
from flask import Flask

from .extensions import db
from .services import seed_demo_records


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
            created = seed_demo_records()
        if created:
            click.echo("Demo data created.")
            return
        click.echo("Demo data already exists.")
