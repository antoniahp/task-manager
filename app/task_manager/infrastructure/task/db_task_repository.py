from typing import Optional, List
from uuid import UUID

from django.db.models import Q

from task_manager.domain.task.task import Task
from task_manager.domain.task.task_repository import TaskRepository


class DbTaskRepository(TaskRepository):
    def filter_task_by_id(self, task_id: UUID) -> Optional[Task]:
        task = Task.objects.filter(id=task_id).first()
        return task

    def filter_task(self, task_id: Optional[UUID] = None, title:Optional[str] = None, estimation: Optional[int] = None, completed: Optional[bool] = None,
                    category:Optional[str] = None, parent_task_id=Optional[UUID], sprint_id: Optional[UUID] = None, user_id: Optional[UUID] = None  ) -> List[Task]:
        filters = Q()
        if task_id is not None:
            filters = filters & Q(id=task_id)
        if title is not None:
            filters = filters & Q(title=title)
        if estimation is not None:
            filters = filters & Q(estimation=estimation)
        if completed is not None:
            filters = filters & Q(completed=completed)
        if category is not None:
            filters = filters & Q(category=category)
        if parent_task_id is not None:
            filters = filters & Q(parent_task_id=parent_task_id)
        if sprint_id is not None:
            filters = filters & Q(sprint_id=sprint_id)
        if user_id is not None:
            filters = filters & Q(user_id=user_id)

        tasks = Task.objects.filter(filters)
        return tasks


    def save_task(self, task: Task) -> None:
        task.save()
