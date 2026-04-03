import os
from flask import Flask, render_template, request, session, redirect, url_for
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
bcrypt = Bcrypt(app)

# Manager credentials loaded from environment variables (never hardcoded)
MANAGER_EMAIL: str = os.getenv("MANAGER_EMAIL", "")
MANAGER_PASSWORD_HASH: str = os.getenv("MANAGER_PASSWORD_HASH", "")


def is_logged_in() -> bool:
    """Check if the manager is currently logged in via session."""
    return session.get("logged_in", False)


@app.route("/")
def login():
    """Display the login page. Redirect to dashboard if already logged in."""
    if is_logged_in():
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/connexion", methods=["POST"])
def connexion():
    """Handle login form submission and verify credentials."""
    email: str = request.form.get("email", "")
    mdp: str = request.form.get("mdp", "")

    # Verify email and bcrypt-hashed password
    if email == MANAGER_EMAIL and bcrypt.check_password_hash(
        MANAGER_PASSWORD_HASH, mdp
    ):
        session["logged_in"] = True
        session["email"] = email
        return redirect(url_for("dashboard"))

    return render_template(
        "login.html", erreur="Email ou mot de passe incorrect !"
    )


@app.route("/dashboard")
def dashboard():
    """Display the dashboard. Requires authentication."""
