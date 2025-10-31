from flask import Blueprint, request, jsonify, session, redirect, render_template
from services.user_service import UserService
from repositories.user_repository import UserRepository

auth_bp = Blueprint("auth", __name__)
svc = UserService(UserRepository())

# ---------- Sign Up ----------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        # If user already logged in, go to app
        if session.get("user_id"):
            return redirect("/app")
        return render_template("auth.html")

    data = request.get_json() if request.is_json else request.form
    email = data.get("email", "").strip().lower()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not email or not username or not password:
        if request.is_json:
            return jsonify({"error": "email, username, and password required"}), 400
        return render_template("auth.html", error="All fields are required.")

    try:
        user = svc.signup(email, username, password)
    except ValueError as e:
        if request.is_json:
            return jsonify({"error": str(e)}), 400
        return render_template("auth.html", error=str(e))

    session["user_id"] = user.id

    # Redirect after successful signup
    if request.is_json:
        return jsonify({"message": "signed up", "redirect": "/app"}), 201
    return redirect("/app")


# ---------- Login ----------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect("/app")
        return render_template("auth.html")

    data = request.get_json() if request.is_json else request.form
    uid = data.get("email_or_username", "").strip().lower()
    password = data.get("password", "")

    if not uid or not password:
        if request.is_json:
            return jsonify({"error": "email_or_username and password required"}), 400
        return render_template("auth.html", error="Both fields are required.")

    try:
        user = svc.login(uid, password)
    except ValueError as e:
        if request.is_json:
            return jsonify({"error": str(e)}), 401
        return render_template("auth.html", error=str(e))

    session["user_id"] = user.id

    if request.is_json:
        return jsonify({"message": "logged in", "redirect": "/app"}), 200
    return redirect("/app")


# ---------- Logout ----------
@auth_bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("user_id", None)
    if request.is_json:
        return jsonify({"message": "logged out", "redirect": "/"}), 200
    return redirect("/")


# ---------- Current User ----------
@auth_bp.get("/me")
def me():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"user": None}), 200

    from models.user import User
    from db import db

    user = db.session.get(User, uid)
    return jsonify({"user": user.to_public() if user else None}), 200
