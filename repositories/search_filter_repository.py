# repositories/search_filter_repository.py
from __future__ import annotations
from typing import Optional, Tuple, List
from sqlalchemy import or_
from db import db
from models.task import Task, SubTask

class SearchFilterRepository:
    """Query helpers and bulk task-completion toggles for tasks/subtasks."""

    # ---------- Derived status ----------
    @staticmethod
    def _is_task_completed(task: Task) -> bool:
        subs = task.subtasks or []
        return len(subs) > 0 and all(st.done for st in subs)

    # ---------- Search & Filter ----------
    def list_tasks_search_filter(
        self,
        user_id: int,
        text: Optional[str] = None,
        status: Optional[str] = None,     # "in_progress" | "completed"
        sort: Optional[str] = None,       # created_asc|created_desc|due_asc|due_desc|title_asc|title_desc
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List[Task], int]:
        q = Task.query.filter_by(user_id=user_id)

        if text:
            like = f"%{text.strip()}%"
            q = q.filter(
                or_(
                    Task.title.ilike(like),
                    Task.description.ilike(like),
                    Task.notes.ilike(like),
                )
            )

        # sorting
        if sort in ("created_asc", "created_desc"):
            q = q.order_by(Task.created_at.asc() if sort.endswith("asc") else Task.created_at.desc())
        elif sort in ("due_asc", "due_desc"):
            q = q.order_by(Task.due_date.asc() if sort.endswith("asc") else Task.due_date.desc())
        elif sort in ("title_asc", "title_desc"):
            q = q.order_by(Task.title.asc() if sort.endswith("asc") else Task.title.desc())
        else:
            q = q.order_by(Task.created_at.desc())  # default

        total_before = q.count()
        items = q.offset((page - 1) * page_size).limit(page_size).all()

        # derived status filtering (after fetch)
        if status in ("completed", "in_progress"):
            items = [
                t for t in items
                if ("completed" if self._is_task_completed(t) else "in_progress") == status
            ]
            total = len(items)
        else:
            total = total_before

        return items, total

    # ---------- Task completion / reopen ----------
    def set_task_status(self, user_id: int, task_id: int, status: str) -> Task:
        t = Task.query.filter_by(user_id=user_id, id=task_id).first()
        if not t:
            raise ValueError("Task not found.")

        make_done = (status == "completed")
        for st in t.subtasks:
            st.done = bool(make_done)
            db.session.add(st)

        db.session.commit()
        db.session.refresh(t)
        return t
