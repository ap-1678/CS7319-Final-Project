# presentation/search_filter_routes.py
from __future__ import annotations
from flask import Blueprint, request, jsonify, session
from services.search_filter_service import SearchFilterService
from repositories.search_filter_repository import SearchFilterRepository

search_filter_bp = Blueprint("search_filter", __name__)
svc = SearchFilterService(SearchFilterRepository())

def login_required_json():
    uid = session.get("user_id")
    if not uid:
        return None, (jsonify({"error": "Unauthorized"}), 401)
    return uid, None

# ---- GET /tasks/search ---------------------------------------------------------
@search_filter_bp.get("/tasks/search")
def search_tasks():
    uid, err = login_required_json()
    if err: return err

    args = request.args
    text = args.get("text")
    status = args.get("status")  # "in_progress" | "completed"
    sort = args.get("sort")      # created_asc|created_desc|due_asc|due_desc|title_asc|title_desc
    try:
        page = int(args.get("page", 1))
        page_size = int(args.get("page_size", 10))
    except ValueError:
        return jsonify({"error": "page and page_size must be integers"}), 400

    items, total = svc.search_filter_tasks(uid, text, status, sort, page, page_size)
    return jsonify({"items": items, "total": total}), 200

# ---- POST /tasks/<id>/complete -------------------------------------------------
@search_filter_bp.post("/tasks/<int:task_id>/complete")
def complete_task(task_id: int):
    uid, err = login_required_json()
    if err: return err
    try:
        data = svc.complete_task(uid, task_id)
        return jsonify({"task": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# ---- POST /tasks/<id>/reopen ---------------------------------------------------
@search_filter_bp.post("/tasks/<int:task_id>/reopen")
def reopen_task(task_id: int):
    uid, err = login_required_json()
    if err: return err
    try:
        data = svc.reopen_task(uid, task_id)
        return jsonify({"task": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
