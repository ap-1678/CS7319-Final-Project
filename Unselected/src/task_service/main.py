from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

app = FastAPI(title="task-service", version="0.1.0")

class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[str] = None  # keep simple for now
    user_id: int

class TaskOut(TaskIn):
    id: int

DB: Dict[int, TaskOut] = {}
_next_id = 1

@app.get("/health")
def health():
    return {"status": "ok", "service": "task-service"}

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(t: TaskIn):
    global _next_id
    task = TaskOut(id=_next_id, **t.dict())
    DB[_next_id] = task
    _next_id += 1
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in DB:
        raise HTTPException(status_code=404, detail="not found")
    del DB[task_id]
    return
