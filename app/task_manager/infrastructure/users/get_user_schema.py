from uuid import UUID

from ninja import Schema


class GetUserSchema(Schema):
    user_id: UUID
    name: str
    company: UUID