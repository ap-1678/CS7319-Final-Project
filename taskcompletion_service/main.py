from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "app.sqlite3")

app = FastAPI(title="task-completion-service", version="0.3.0")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

class SubtaskIn(BaseModel):
    title: str

class TaskIn(BaseModel):
    title: str
    subtasks: Optional[List[SubtaskIn]] = None
    completed: bool = False   # used only when there are no subtasks

@app.get("/health")
def health():
    return {"status": "ok", "service": "task-completion-service"}

@app.post("/tasks", status_code=201)
def create_task(t: TaskIn):
    with get_conn() as c:
        cur = c.execute(
            "INSERT INTO tasks(title, description, category, due_date, created_at, completed) "
            "VALUES(?,?,?,?,?,?)",
            (t.title, None, None, None, datetime.utcnow().timestamp(), int(t.completed))
        )
        tid = cur.lastrowid
        for s in (t.subtasks or []):
            c.execute("INSERT INTO subtasks(task_id,title,done) VALUES(?,?,0)", (tid, s.title))
    return {"id": tid}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_conn() as c:
        t = c.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not t:
            raise HTTPException(404, "not found")
        subs = c.execute("SELECT id,title,done FROM subtasks WHERE task_id=?", (task_id,)).fetchall()
        if subs:
            all_done = c.execute("SELECT SUM(done)=COUNT(*) AS all_done FROM subtasks WHERE task_id=?", (task_id,)).fetchone()["all_done"]
            status = "completed" if all_done == 1 else "in_progress"
        else:
            status = "completed" if t["completed"] == 1 else "in_progress"
        return {
            "id": t["id"], "title": t["title"], "created_at": t["created_at"],
            "status": status,
            "subtasks": [{"id": s["id"], "title": s["title"], "done": bool(s["done"])} for s in subs]
        }

@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    with get_conn() as c:
        t = c.execute("SELECT id FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not t: raise HTTPException(404, "not found")
        # if subtasks exist -> set all done=1, else set tasks.completed=1
        sub_count = c.execute("SELECT COUNT(*) AS c FROM subtasks WHERE task_id=?", (task_id,)).fetchone()["c"]
        if sub_count > 0:
            c.execute("UPDATE subtasks SET done=1 WHERE task_id=?", (task_id,))
        else:
            c.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
    return {"status": "ok", "task_id": task_id}

@app.post("/tasks/{task_id}/reopen")
def reopen_task(task_id: int):
    with get_conn() as c:
        t = c.execute("SELECT id FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not t: raise HTTPException(404, "not found")
        sub_count = c.execute("SELECT COUNT(*) AS c FROM subtasks WHERE task_id=?", (task_id,)).fetchone()["c"]
        if sub_count > 0:
            c.execute("UPDATE subtasks SET done=0 WHERE task_id=?", (task_id,))
        else:
            c.execute("UPDATE tasks SET completed=0 WHERE id=?", (task_id,))
    return {"status": "ok", "task_id": task_id}
