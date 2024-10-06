from abc import abstractmethod, ABC
from datetime import date
from typing import Optional, List
from uuid import UUID

from task_manager.domain.sprint.sprint import Sprint


class SprintRepository(ABC):
    @abstractmethod
    def filter_sprint_by_id (self, sprint_id: UUID) -> Optional[Sprint]:
        pass
    @abstractmethod
    def filter_sprint(self, company_id: Optional[UUID] = None, sprint_id: Optional[UUID] = None, name: Optional[str] = None,
                      start_date: Optional[date] = None, end_date: Optional[date] = None, objective: Optional[str] = None, active: Optional[bool] = None) -> List[Sprint]:
        pass

    @abstractmethod
    def save_sprint(self, sprint: Sprint) -> None:
        pass
