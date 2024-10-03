from typing import Optional
from uuid import UUID

from task_manager.domain.task.task import Task


class TaskCreator:
    def create_task(self, task_id: UUID, title:str, description:str, estimation: int, completed: bool, category:str, parent_task: Optional[UUID] = None, sprint: Optional[UUID] = None, project: Optional[UUID] = None, user: Optional[UUID] = None ) -> Task:
        return Task(
            task_id=task_id,
            title=title,
            description=description,
            estimation=estimation,
            completed=completed,
            category=category,
            parent_task=parent_task,
            sprint=sprint,
            project=project,
            user=user
        )