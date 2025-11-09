# search_filter_service/main.py
from __future__ import annotations
import os
import sqlite3
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Any, Annotated
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

# ---------- DB ----------
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "app.sqlite3")

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ---------- App ----------
app = FastAPI(title="search-filter-service", version="0.6.0", docs_url="/docs", redoc_url="/redoc")

# ---------- Enums ----------
class StatusEnum(str, Enum):
    completed = "completed"
    in_progress = "in_progress"

class SortEnum(str, Enum):
    created_asc = "created_asc"
    created_desc = "created_desc"
    due_asc = "due_asc"
    due_desc = "due_desc"
    title_asc = "title_asc"
    title_desc = "title_desc"

StatusChoices = [e.value for e in StatusEnum]
SortChoices = [e.value for e in SortEnum]

StatusParam = Annotated[Optional[str], Query(description="completed | in_progress", enum=StatusChoices)]
SortParam   = Annotated[str,         Query(description="Sort order",            enum=SortChoices)]

# ---------- Models ----------
class SubtaskIn(BaseModel):
    title: str

class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    completed: bool = False
    subtasks: Optional[List[SubtaskIn]] = None

# ---------- Utils ----------
def _now_epoch() -> float:
    return datetime.now(timezone.utc).timestamp()

def _date_str_from_epoch(epoch: Optional[float]) -> Optional[str]:
    if epoch is None:
        return None
    try:
        return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return None

# ---------- Routes ----------
@app.get("/health")
def health():
    return {"status": "ok", "service": "search-filter-service"}

@app.post("/tasks", status_code=201)
def create_task(t: TaskIn):
    with get_conn() as c:
        cur = c.execute(
            "INSERT INTO tasks (title, description, due_date, created_at, completed) VALUES (?,?,?,?,?)",
            (t.title, t.description, t.due_date, _now_epoch(), int(t.completed)),
        )
        tid = cur.lastrowid
        for s in (t.subtasks or []):
            c.execute("INSERT INTO subtasks (task_id, title, done) VALUES (?,?,0)", (tid, s.title))
    return {"id": tid}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_conn() as c:
        t = c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not t:
            raise HTTPException(status_code=404, detail="not found")

        subs = c.execute("SELECT id, title, done FROM subtasks WHERE task_id = ?", (task_id,)).fetchall()
        total = len(subs)
        done_count = sum(1 for s in subs if s["done"])
        status = "completed" if (total > 0 and done_count == total) or (total == 0 and t["completed"]) else "in_progress"

        return {
            "id": t["id"],
            "title": t["title"],
            "description": t["description"],
            "due_date": t["due_date"],
            "created_date": _date_str_from_epoch(t["created_at"]),  # 👈 readable date
            "status": status,
            "subtasks": [{"id": s["id"], "title": s["title"], "done": bool(s["done"])} for s in subs],
            "subtasks_summary": {"total": total, "done": done_count},
        }

@app.get("/search")
def search_tasks(
    text: Optional[str] = Query(default=None, description="Search by title, description, or subtask"),
    status: StatusParam = None,
    sort:   SortParam   = SortEnum.created_desc.value,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
):
    try:
        sort_enum = SortEnum(sort)
        status_enum = StatusEnum(status) if status else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid sort or status value")

    order_sql = {
        SortEnum.created_asc:  "ORDER BY t.created_at ASC",
        SortEnum.created_desc: "ORDER BY t.created_at DESC",
        SortEnum.due_asc:      "ORDER BY (t.due_date IS NULL), t.due_date ASC",
        SortEnum.due_desc:     "ORDER BY (t.due_date IS NULL), t.due_date DESC",
        SortEnum.title_asc:    "ORDER BY LOWER(t.title) ASC",
        SortEnum.title_desc:   "ORDER BY LOWER(t.title) DESC",
    }[sort_enum]

    where, params = [], []
    if text:
        like = f"%{text.lower()}%"
        where.append("(LOWER(t.title) LIKE ? OR LOWER(t.description) LIKE ? OR EXISTS (SELECT 1 FROM subtasks s WHERE s.task_id=t.id AND LOWER(s.title) LIKE ?))")
        params += [like, like, like]
    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    with get_conn() as c:
        tasks = c.execute(
            f"SELECT * FROM tasks t {where_sql} {order_sql} LIMIT ? OFFSET ?",
            params + [page_size, (page - 1) * page_size],
        ).fetchall()

        items: List[dict] = []
        for t in tasks:
            subs = c.execute("SELECT id, title, done FROM subtasks WHERE task_id = ?", (t["id"],)).fetchall()
            total = len(subs)
            done_count = sum(1 for s in subs if s["done"])
            derived_status = "completed" if (total > 0 and done_count == total) or (total == 0 and t["completed"]) else "in_progress"

            if status_enum and derived_status != status_enum.value:
                continue

            items.append({
                "id": t["id"],
                "title": t["title"],
                "description": t["description"],
                "due_date": t["due_date"],
                "created_date": _date_str_from_epoch(t["created_at"]),  # 👈 readable date
                "status": derived_status,
                "subtasks": [{"id": s["id"], "title": s["title"], "done": bool(s["done"])} for s in subs],
                "subtasks_summary": {"total": total, "done": done_count},
            })

        total = len(items)
        return {"items": items, "total": total}
