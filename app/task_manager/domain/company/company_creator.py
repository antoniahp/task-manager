from uuid import UUID

from task_manager.domain.company.company import Company


class CompanyCreator:
    def create_company(self, company_id: UUID, name: str) -> Company:
        return Company(
            id=company_id,
            name=name
        )