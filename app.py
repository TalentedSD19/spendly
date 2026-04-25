from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import (
    get_db, init_db, seed_db, create_user, get_user_by_email,
    get_user_by_id, update_user,
)
from database.queries import (
    get_user_by_id      as get_user_profile,
    get_summary_stats,
    get_recent_transactions,
    get_category_breakdown,
)

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm:
            return render_template("register.html", error="All fields are required.")
        if password != confirm:
            return render_template("register.html", error="Passwords do not match.")

        try:
            create_user(name, email, generate_password_hash(password))
        except Exception:
            return render_template("register.html", error="That email is already registered.")

        flash("Account created! Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            return render_template("login.html", error="All fields are required.")

        user = get_user_by_email(email)
        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password.")

        session.clear()
        session["user_id"]   = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You've been signed out.", "success")
    return redirect(url_for("landing"))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "update_name":
            new_name = request.form.get("name", "").strip()
            if not new_name:
                flash("Name cannot be empty.", "error")
                return redirect(url_for("profile"))
            update_user(session["user_id"], new_name, None)
            session["user_name"] = new_name
            flash("Name updated successfully.", "success")
            return redirect(url_for("profile"))

        elif action == "change_password":
            current_pw = request.form.get("current_password", "")
            new_pw     = request.form.get("new_password", "")
            confirm_pw = request.form.get("confirm_password", "")
            user = get_user_by_id(session["user_id"])
            if not check_password_hash(user["password_hash"], current_pw):
                flash("Current password is incorrect.", "error")
                return redirect(url_for("profile"))
            if len(new_pw) < 8:
                flash("New password must be at least 8 characters.", "error")
                return redirect(url_for("profile"))
            if new_pw != confirm_pw:
                flash("Passwords do not match.", "error")
                return redirect(url_for("profile"))
            update_user(session["user_id"], user["name"], generate_password_hash(new_pw))
            flash("Password changed successfully.", "success")
            return redirect(url_for("profile"))

        flash("Invalid action.", "error")
        return redirect(url_for("profile"))

    user = get_user_profile(session["user_id"])
    if user is None:
        session.clear()
        return redirect(url_for("login"))

    stats     = get_summary_stats(session["user_id"])
    breakdown = get_category_breakdown(session["user_id"])
    recent    = get_recent_transactions(session["user_id"], limit=10)

    parts    = user["name"].split()
    initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        breakdown=breakdown,
        recent=recent,
        initials=initials,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


with app.app_context():
    init_db()
    seed_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
