from flask import Flask, render_template
from flask.typing import ResponseReturnValue

app = Flask(__name__)


@app.route("/")
def home() -> ResponseReturnValue:
    return render_template("home.html")


@app.route("/login")
def login() -> ResponseReturnValue:
    return render_template("login.html")


@app.route("/dashboard")
def dashboard() -> ResponseReturnValue:
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
