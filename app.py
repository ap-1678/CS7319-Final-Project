'''
CS7319 Group 7
Layered Architecture (using Python/Flask):
Presentation (routes) → Service (rules) → Repository (DB I/O) → Database (SQLite via SQLAlchemy)

taskmgr_layered/
├─ app.py
├─ db.py
├─ models/
│  └─ user.py
├─ repositories/
│  └─ user_repository.py
├─ services/
│  └─ user_service.py
└─ presentation/
   └─ auth_routes.py

1. Start app: python app.py
2. Visit http://127.0.0.1:5000/ for the page.
3. Sign Up (creates a profile and auto-logs in).

Layered Architecture (Flask) app with a real Task Manager that appears after login,
supports main tasks and sub-tasks, and computes overall progress from sub-tasks.

4. After login/sign-up, users are sent to /app (a simple Task Manager UI).
Tasks: title, description, due date, notes.
Sub-tasks: title, description, priority, due date, done/undone.
Progress: if a task has sub-tasks, progress = done / total (as a %).
If no sub-tasks, progress is 0%.
'''
from flask import Flask, render_template, redirect, session
from db import init_db
from presentation.auth_routes import auth_bp
from presentation.tasks_routes import tasks_bp
from presentation.search_filter_routes import search_filter_bp
from presentation.task_completion_routes import task_completion_bp



def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskmgr.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "change-me-in-prod"
    init_db(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp)  # serves /app and /tasks APIs
    app.register_blueprint(search_filter_bp)
    app.register_blueprint(task_completion_bp)

    @app.route("/")
    def home():
        # If logged in, go straight to Task Manager; else show auth page.
        if session.get("user_id"):
            return redirect("/app")
        return render_template("auth.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
