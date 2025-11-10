from flask import Blueprint, request, jsonify, session, render_template, redirect
from services.task_service import TaskService
from repositories.task_repository import TaskRepository

tasks_bp = Blueprint("tasks", __name__)
svc = TaskService(TaskRepository())

def login_required_json():
    uid = session.get("user_id")
    if not uid:
        return None, (jsonify({"error": "Unauthorized"}), 401)
    return uid, None

@tasks_bp.get("/app")
def app_page():
    if not session.get("user_id"):
        return redirect("/")
    return render_template("app.html")  # Task Manager UI

@tasks_bp.get("/tasks")
def list_tasks():
    uid, err = login_required_json()
    if err: return err
    items = svc.list_tasks(uid)
    return jsonify({"tasks": items})

@tasks_bp.post("/tasks")
def create_task():
    uid, err = login_required_json()
    if err: return err
    data = request.json or {}
    try:
        item = svc.create_task(
            uid,
            title=data.get("title", ""),
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            notes=data.get("notes", ""),
        )
        return jsonify({"task": item}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@tasks_bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    uid, err = login_required_json()
    if err: return err
    try:
        svc.delete_task(uid, task_id)
        return jsonify({"message": "deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@tasks_bp.post("/tasks/<int:task_id>/subtasks")
def add_subtask(task_id):
    uid, err = login_required_json()
    if err: return err
    data = request.json or {}
    try:
        st = svc.add_subtask(
            uid, task_id,
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=int(data.get("priority", 3)),
            due_date=data.get("due_date"),
        )
        return jsonify({"subtask": st}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@tasks_bp.delete("/tasks/<int:task_id>/subtasks/<int:subtask_id>")
def delete_subtask(task_id, subtask_id):
    uid, err = login_required_json()
    if err: return err
    try:
        svc.delete_subtask(uid, task_id, subtask_id)
        return jsonify({"message": "deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@tasks_bp.post("/tasks/<int:task_id>/subtasks/<int:subtask_id>/toggle")
def toggle_subtask(task_id, subtask_id):
    uid, err = login_required_json()
    if err: return err
    data = request.json or {}
    try:
        st = svc.toggle_subtask(uid, task_id, subtask_id, bool(data.get("done", True)))
        return jsonify({"subtask": st}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
