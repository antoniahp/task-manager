from uuid import UUID

from ninja import Schema


class GetCompanySchema(Schema):
    company_id: UUID
    name: str