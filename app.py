from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
from functools import wraps
import os

app = Flask(__name__)

# --------------------------------
# Secret Key
# --------------------------------

app.secret_key = "SecureShield-Secret-Key-2026"


# --------------------------------
# Login Credentials
# --------------------------------

USERNAME = "admin"
PASSWORD = "admin@123"


# --------------------------------
# Login Required
# --------------------------------

def login_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if not session.get("logged_in"):
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view


# --------------------------------
# Login Page
# --------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:

            session["logged_in"] = True

            # IMPORTANT:
            # After login, go to WEBSITE HOME
            # NOT dashboard

            return redirect(url_for("home"))

        else:

            error = "Invalid username or password."

    return render_template(
        "login.html",
        error=error
    )


# --------------------------------
# Logout
# --------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# --------------------------------
# Home Page
# --------------------------------

@app.route("/")
@login_required
def home():

    return render_template("index.html")


# --------------------------------
# About Page
# --------------------------------

@app.route("/about")
@login_required
def about():

    return render_template("about.html")
@app.route("/profile")
@login_required
def profile():

    return render_template("profile.html")
@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")

        session["username"] = username
        session["email"] = email

        return redirect(url_for("profile"))

    return render_template("edit-profile.html")
@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    error = None
    success = None

    if request.method == "POST":

        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if current_password != PASSWORD:
            error = "Current password is incorrect."

        elif new_password != confirm_password:
            error = "New passwords do not match."

        elif len(new_password) < 8:
            error = "New password must be at least 8 characters."

        else:
            success = "Password changed successfully."

    return render_template(
        "change-password.html",
        error=error,
        success=success
    )

# --------------------------------
# Download
# --------------------------------

@app.route("/download")
@login_required
def download():

    downloads_folder = os.path.join(
        app.root_path,
        "downloads"
    )

    return send_from_directory(
        downloads_folder,
        "SecureShield_Setup.exe",
        as_attachment=True
    )


# --------------------------------
# Feature Pages
# --------------------------------

PAGES = {

    "system-monitor": "system-monitor.html",

    "process-monitor": "process-monitor.html",

    "suspicious-activity": "suspicious-activity.html",

    "network-monitor": "network-monitor.html",

    "port-monitor": "port-monitor.html",

    "file-integrity": "file-integrity.html",

    "security-logging": "security-logging.html",

    "alerts": "alerts.html",

    "dashboard": "dashboard.html"
}


def make_view(template):

    @login_required
    def view():

        return render_template(template)

    return view


for slug, template in PAGES.items():

    app.add_url_rule(
        "/" + slug,
        slug,
        make_view(template)
    )


# --------------------------------
# Start Website
# --------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )