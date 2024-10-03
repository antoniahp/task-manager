from uuid import UUID
from ninja import Schema

class IdentifierSchema(Schema):
    id: UUID