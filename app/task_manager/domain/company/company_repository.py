from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from task_manager.domain.company.company import Company


class CompanyRepository(ABC):
    @abstractmethod
    def filter_company_by_id(self, company_id: UUID) -> Optional[Company]:
        pass

    @abstractmethod
    def filter_company(self, company_id: Optional[UUID]=None, name: Optional[str]=None , requester_user_id: Optional[UUID]=None) -> Optional[Company]:
        pass

    @abstractmethod
    def save_company(self, company: Company) -> None:
        pass