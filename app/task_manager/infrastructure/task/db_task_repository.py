from datetime import datetime
from typing import Optional, List
from uuid import UUID

from django.db.models import Q

from task_manager.domain.task.task import Task
from task_manager.domain.task.task_repository import TaskRepository


class DbTaskRepository(TaskRepository):
    def filter_task_by_id(self, task_id: UUID) -> Optional[Task]:
        task = Task.objects.filter(id=task_id).first()
        return task

    def filter_task(self,  task_id: Optional[UUID] = None,
                    title:Optional[str] = None,
                    estimation: Optional[int] = None,
                    completed: Optional[bool] = None,
                    user_story_id: Optional[UUID] = None,
                    sprint_id: Optional[UUID] = None,
                    assigned_user_id: Optional[UUID] = None,
                    status_column_id: Optional[UUID] = None,
                    completed_at:Optional[datetime] = None,
                    completed_at__gte:Optional[datetime] = None,
                    completed_at__lte:Optional[datetime] = None)  -> List[Task]:
        filters = Q()
        if task_id is not None:
            filters = filters & Q(id=task_id)
        if title is not None:
            filters = filters & Q(title=title)
        if estimation is not None:
            filters = filters & Q(estimation=estimation)
        if completed is not None:
            filters = filters & Q(completed=completed)
        if user_story_id is not None:
            filters = filters & Q(user_story_id=user_story_id)
        if sprint_id is not None:
            filters = filters & Q(sprint_id=sprint_id)
        if assigned_user_id is not None:
            filters = filters & Q(assigned_user_id=assigned_user_id)
        if status_column_id is not None:
            filters = filters & Q(status_column_id=status_column_id)
        if completed_at is not None:
            filters = filters & Q(completed_at=completed_at)
        if completed_at__gte is not None:
            filters = filters & Q(completed_at__gte=completed_at__gte)
        if completed_at__lte is not None:
            filters = filters & Q(completed_at__lte=completed_at__lte)

        tasks = Task.objects.filter(filters)
        return tasks


    def save_task(self, task: Task) -> None:
        task.save()
