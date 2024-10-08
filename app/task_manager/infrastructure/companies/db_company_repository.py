from typing import Optional, List
from uuid import UUID

from django.db.models import Q

from task_manager.domain.company.company import Company
from task_manager.domain.company.company_repository import CompanyRepository


class DbCompanyRepository(CompanyRepository):

    def filter_company_by_id(self, company_id: UUID) -> Optional[Company]:
        company = Company.objects.filter(id=company_id).first()
        return company


    def filter_company(self, company_id: Optional[UUID]=None, name: Optional[str]=None , requester_user_id: Optional[UUID]=None) -> List[Company]:
        filters = Q()
        if company_id is not None:
            filters = filters & Q(id=company_id)
        if requester_user_id is not None:
            filters = filters & Q(users=requester_user_id)
        if name is not None:
            filters = filters & Q(name=name)
        companies = Company.objects.filter(filters)
        return companies




    def save_company(self, company: Company) -> None:
        company.save()