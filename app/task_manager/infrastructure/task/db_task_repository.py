from typing import Optional, List
from uuid import UUID

from django.db.models import Q

from task_manager.domain.task.task import Task
from task_manager.domain.task.task_repository import TaskRepository


class DbTaskRepository(TaskRepository):

    def filter_task(self, task_id: Optional[UUID] = None, title:Optional[str] = None, estimation: Optional[int] = None, completed: Optional[bool] = None,
                    category:Optional[str] = None, sprint: Optional[UUID] = None, user: Optional[UUID] = None ) -> List[Task]:
        filters = Q()
        if task_id is not None:
            filters = filters & Q(task_id=task_id)
        if title is not None:
            filters = filters & Q(title=title)
        if estimation is not None:
            filters = filters & Q(estimation=estimation)
        if completed is not None:
            filters = filters & Q(completed=completed)
        if category is not None:
            filters = filters & Q(category=category)
        if sprint is not None:
            filters = filters & Q(sprint=sprint)
        if user is not None:
            filters = filters & Q(user=user)

        tasks = Task.objects.filter(filters)
        return tasks


    def save_task(self, task: Task) -> None:
        task.save()
