from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from task_manager.domain.status_column.status_column import StatusColumn


class StatusColumnRepository(ABC):
    @abstractmethod
    def filter_status_column_by_id(self, status_column_id: UUID) -> Optional[StatusColumn]:
        pass

    @abstractmethod
    def filter_status_columns(self, status_column_id: Optional[UUID], name: Optional[str], company_id: Optional[UUID], order: Optional[int]) -> Optional[StatusColumn]:
        pass

    @abstractmethod
    def save_status_column(self, status_column: StatusColumn):
        pass