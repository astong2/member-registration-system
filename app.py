import os
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------------------
# App & DB config
# ---------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "members.db")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY", "dev-change-me")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------------------
# Model
# ---------------------------
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)


# Ensure DB exists
with app.app_context():
    db.create_all()


# ---------------------------
# Helpers
# ---------------------------
def login_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapper


# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    logged_in = "user_id" in session
    return render_template("home.html", logged_in=logged_in)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        # Check uniqueness
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.", "error")
            return redirect(url_for("register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Logged in successfully!", "success")
            return redirect(url_for("profile"))

        flash("Invalid username or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    user = User.query.get(session["user_id"])
    return render_template("profile.html", user=user)


@app.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    user = User.query.get(session["user_id"])
    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash("Your account has been deleted.", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    # Dev server
    app.run(debug=True)
