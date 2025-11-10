from typing import Optional
from datetime import datetime
from repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def _parse_date(self, s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        try:
            # Accept ISO8601 or 'YYYY-MM-DD'
            return datetime.fromisoformat(s)
        except Exception:
            try:
                return datetime.strptime(s, "%Y-%m-%d")
            except Exception:
                raise ValueError("Invalid date format. Use ISO 8601 or YYYY-MM-DD.")

    def list_tasks(self, user_id: int):
        return [t.to_public() for t in self.repo.list_by_user(user_id)]

    def create_task(self, user_id: int, title: str, description: str, due_date: Optional[str], notes: str):
        if not title.strip():
            raise ValueError("Title is required.")
        dt = self._parse_date(due_date)
        t = self.repo.create_task(user_id, title.strip(), description or "", dt, notes or "")
        return t.to_public()

    def delete_task(self, user_id: int, task_id: int):
        t = self.repo.get_task_for_user(user_id, task_id)
        if not t:
            raise ValueError("Task not found.")
        self.repo.delete_task(t)

    def add_subtask(self, user_id: int, task_id: int, title: str, description: str, priority: int, due_date: Optional[str]):
        t = self.repo.get_task_for_user(user_id, task_id)
        if not t:
            raise ValueError("Task not found.")
        if not title.strip():
            raise ValueError("Sub-task title is required.")
        if priority not in (1, 2, 3):
            raise ValueError("Priority must be 1 (High), 2 (Medium), or 3 (Low).")
        dt = self._parse_date(due_date)
        st = self.repo.add_subtask(t, title.strip(), description or "", priority, dt)
        return st.to_public()

    def delete_subtask(self, user_id: int, task_id: int, subtask_id: int):
        t = self.repo.get_task_for_user(user_id, task_id)
        if not t:
            raise ValueError("Task not found.")
        st = self.repo.get_subtask(t, subtask_id)
        if not st:
            raise ValueError("Sub-task not found.")
        self.repo.delete_subtask(st)

    def toggle_subtask(self, user_id: int, task_id: int, subtask_id: int, done: bool):
        t = self.repo.get_task_for_user(user_id, task_id)
        if not t:
            raise ValueError("Task not found.")
        st = self.repo.get_subtask(t, subtask_id)
        if not st:
            raise ValueError("Sub-task not found.")
        st = self.repo.toggle_subtask_done(st, done)
        return st.to_public()
