from __future__ import annotations

import os
from typing import Any

from flask import Flask

DEFAULT_HUGGING_FACE_MODEL_URL = (
    "https://api-inference.huggingface.co/models/" "HuggingFaceTB/SmolLM2-1.7B-Instruct"
)


def normalize_database_url(database_url: str) -> str:
    """Convert postgres:// URLs for SQLAlchemy compatibility."""
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql://", 1)
    return database_url


def configure_app(app: Flask, test_config: dict[str, Any] | None = None) -> None:
    """Load configuration values for local, test, and production usage."""
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
