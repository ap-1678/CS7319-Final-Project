# repositories/task_completion_repository.py
from __future__ import annotations
from db import db
from models.task import Task

class TaskCompletionRepository:
    """Bulk complete/reopen operations at the task level."""

    def set_task_status(self, user_id: int, task_id: int, status: str) -> Task:
        """
        Sets all subtasks under the task to done=True (completed) or False (reopen).
        We derive the task's 'completed' state from subtasks.
        """
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
