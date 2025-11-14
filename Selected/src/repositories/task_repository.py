from typing import List, Optional
from db import db
from models.task import Task, SubTask
from datetime import datetime

class TaskRepository:
    def list_by_user(self, user_id: int) -> List[Task]:
        return Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()

    def get_task_for_user(self, user_id: int, task_id: int) -> Optional[Task]:
        return Task.query.filter_by(user_id=user_id, id=task_id).first()

    def create_task(self, user_id: int, title: str, description: str, due_date: Optional[datetime], notes: str) -> Task:
        t = Task(user_id=user_id, title=title, description=description or "", due_date=due_date, notes=notes or "")
        db.session.add(t)
        db.session.commit()
        db.session.refresh(t)
        return t

    def delete_task(self, task: Task):
        db.session.delete(task)
        db.session.commit()

    def add_subtask(self, task: Task, title: str, description: str, priority: int, due_date: Optional[datetime]) -> SubTask:
        st = SubTask(task_id=task.id, title=title, description=description or "", priority=priority or 3, due_date=due_date)
        db.session.add(st)
        db.session.commit()
        db.session.refresh(st)
        return st

    def get_subtask(self, task: Task, subtask_id: int) -> Optional[SubTask]:
        return SubTask.query.filter_by(task_id=task.id, id=subtask_id).first()

    def delete_subtask(self, subtask: SubTask):
        db.session.delete(subtask)
        db.session.commit()

    def toggle_subtask_done(self, subtask: SubTask, done: bool):
        subtask.done = bool(done)
        db.session.commit()
        db.session.refresh(subtask)
        return subtask
