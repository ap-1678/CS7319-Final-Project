# presentation/task_completion_routes.py
from __future__ import annotations
from flask import Blueprint, request, jsonify, session
from services.task_completion_service import TaskCompletionService
from repositories.task_completion_repository import TaskCompletionRepository

task_completion_bp = Blueprint("task_completion", __name__)
svc = TaskCompletionService(TaskCompletionRepository())

def login_required_json():
    uid = session.get("user_id")
    if not uid:
        return None, (jsonify({"error": "Unauthorized"}), 401)
    return uid, None

# POST /tasks/<id>/complete  -> set all subtasks done=True
@task_completion_bp.post("/tasks/<int:task_id>/complete")
def complete_task(task_id: int):
    uid, err = login_required_json()
    if err: return err
    try:
        data = svc.complete_task(uid, task_id)
        return jsonify({"task": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# POST /tasks/<id>/reopen    -> set all subtasks done=False
@task_completion_bp.post("/tasks/<int:task_id>/reopen")
def reopen_task(task_id: int):
    uid, err = login_required_json()
    if err: return err
    try:
        data = svc.reopen_task(uid, task_id)
        return jsonify({"task": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
