from abc import abstractmethod, ABC
from typing import Optional, List
from uuid import UUID

from task_manager.domain.task.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def filter_task(self, task_id: Optional[UUID] = None, title:Optional[str] = None, estimation: Optional[int] = None, completed: Optional[bool] = None, category:Optional[str] = None, sprint: Optional[UUID] = None, user: Optional[UUID] = None ) -> List[Task]:
        pass

    @abstractmethod
    def save_task(self, task: Task) -> None:
        pass
