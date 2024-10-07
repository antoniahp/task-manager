from uuid import UUID

from ninja import Schema


class GetCompanySchema(Schema):
    id: UUID
    name: str
