from datetime import datetime
from typing import Optional
from uuid import UUID

from task_manager.domain.task.task import Task


class TaskCreator:
    def create_task(self, task_id: UUID, title:str, description:str, estimation: int, completed: bool, completed_at:datetime, category:str, parent_task_id: Optional[UUID] = None, sprint_id: Optional[UUID] = None, project_id: Optional[UUID] = None, user_id: Optional[UUID] = None, status_column_id: Optional[UUID] = None ) -> Task:
        return Task(
            id=task_id,
            title=title,
            description=description,
            estimation=estimation,
            completed=completed,
            category=category,
            parent_task_id=parent_task_id,
            sprint_id=sprint_id,
            project_id=project_id,
            user_id=user_id,
            status_column_id=status_column_id,
            completed_at=completed_at
        )