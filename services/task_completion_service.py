# services/task_completion_service.py
from __future__ import annotations
from typing import Dict, Any
from repositories.task_completion_repository import TaskCompletionRepository

class TaskCompletionService:
    def __init__(self, repo: TaskCompletionRepository):
        self.repo = repo

    def complete_task(self, user_id: int, task_id: int) -> Dict[str, Any]:
        """Marks all subtasks done=True and returns the public task payload."""
        t = self.repo.set_task_status(user_id, task_id, "completed")
        return t.to_public()

    def reopen_task(self, user_id: int, task_id: int) -> Dict[str, Any]:
        """Marks all subtasks done=False and returns the public task payload."""
        t = self.repo.set_task_status(user_id, task_id, "in_progress")
        return t.to_public()
