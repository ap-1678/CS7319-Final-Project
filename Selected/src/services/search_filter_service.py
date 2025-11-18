# services/search_filter_service.py
from __future__ import annotations
from typing import Optional, Tuple, List, Dict, Any
from repositories.search_filter_repository import SearchFilterRepository

class SearchFilterService:
    def __init__(self, repo: SearchFilterRepository):
        self.repo = repo

    def search_filter_tasks(
        self,
        user_id: int,
        text: Optional[str] = None,
        status: Optional[str] = None,   # "in_progress" | "completed"
        sort: Optional[str] = None,     # created_asc|created_desc|due_asc|due_desc|title_asc|title_desc
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List[Dict[str, Any]], int]:
        items, total = self.repo.list_tasks_search_filter(user_id, text, status, sort, page, page_size)

        def to_public_plus(task):
            data = task.to_public()
            subs = getattr(task, "subtasks", []) or []
            done = len(subs) > 0 and all(st.done for st in subs)
            data["status"] = "completed" if done else "in_progress"
            data["subtasks_summary"] = {
                "total": len(subs),
                "done": sum(1 for s in subs if s.done),
            }
            return data

        return [to_public_plus(t) for t in items], total

    # ---- Task completion / reopen ----
    def complete_task(self, user_id: int, task_id: int) -> Dict[str, Any]:
        t = self.repo.set_task_status(user_id, task_id, "completed")
        return t.to_public()

    def reopen_task(self, user_id: int, task_id: int) -> Dict[str, Any]:
        t = self.repo.set_task_status(user_id, task_id, "in_progress")
        return t.to_public()
