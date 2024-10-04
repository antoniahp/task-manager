from abc import abstractmethod, ABC
from typing import Optional, List
from uuid import UUID

from task_manager.domain.task.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def filter_task_by_id(self, task_id: UUID) -> Optional[Task]:
        pass
    @abstractmethod
    def filter_task(self, task_id: Optional[UUID] = None, title:Optional[str] = None, estimation: Optional[int] = None, completed: Optional[bool] = None, category:Optional[str] = None, parent_task_id=Optional[UUID], sprint_id: Optional[UUID] = None, user_id: Optional[UUID] = None ) -> List[Task]:
        pass

    @abstractmethod
    def save_task(self, task: Task) -> None:
        pass
