from abc import abstractmethod, ABC
from datetime import datetime

from typing import Optional, List
from uuid import UUID

from task_manager.domain.task.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def filter_task_by_id(self, task_id: UUID) -> Optional[Task]:
        pass
    @abstractmethod
    def filter_task(self,  task_id: Optional[UUID] = None,
                    title:Optional[str] = None,
                    estimation: Optional[int] = None,
                    completed: Optional[bool] = None,
                    deleted: Optional[bool] = None,
                    user_story_id: Optional[UUID] = None,
                    sprint_id: Optional[UUID] = None,
                    assigned_user_id: Optional[UUID] = None,
                    status_column_id: Optional[UUID] = None,
                    completed_at:Optional[datetime] = None,
                    completed_at__gte:Optional[datetime] = None,
                    completed_at__lte:Optional[datetime] = None,
                    project_id: Optional[UUID] = None)  -> List[Task]:
        pass

    @abstractmethod
    def save_task(self, task: Task) -> None:
        pass
