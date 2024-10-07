from uuid import UUID


class CompanyNotFoundException(Exception):
    def __init__(self, company_id: UUID):
        self.company_id = company_id
        self.message = f"Company with ID {company_id} not found"
        super().__init__(self.message)