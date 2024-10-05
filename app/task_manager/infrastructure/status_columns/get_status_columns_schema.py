from uuid import UUID

from ninja import Schema


class GetStatusColumnsSchema(Schema):
    id: UUID
    name: str
    company_id: UUID
    order: int

