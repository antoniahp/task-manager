from datetime import datetime
from typing import Optional
from uuid import UUID

from task_manager.domain.task.task import Task


class TaskCreator:
    def create_task(self, task_id: UUID, title:str, description:str, estimation: int, completed: bool, completed_at:datetime, user_story_id:UUID, sprint_id: Optional[UUID] = None,  assigned_user_id: Optional[UUID] = None, status_column_id: Optional[UUID] = None ) -> Task:
        return Task(
            id=task_id,
            title=title,
            description=description,
            estimation=estimation,
            completed=completed,
            sprint_id=sprint_id,
            assigned_user_id=assigned_user_id,
            status_column_id=status_column_id,
            completed_at=completed_at,
            user_story_id=user_story_id
        )