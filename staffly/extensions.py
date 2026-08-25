from __future__ import annotations

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
bcrypt = Bcrypt()
