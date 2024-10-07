from uuid import UUID

from ninja import Schema


class GetUserSchema(Schema):
    id: UUID
    name: str
