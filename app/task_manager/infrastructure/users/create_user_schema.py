from uuid import UUID

from ninja import Schema


class CreateUserSchema(Schema):
    name: str
    company: UUID
    password: str
    username: str
    email: str
    password: str
