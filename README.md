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

Prerequisites:
pip install -r requirements.txt

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
