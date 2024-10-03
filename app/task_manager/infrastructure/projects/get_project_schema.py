from datetime import date
from uuid import UUID

from ninja import Schema


class GetProjectSchema(Schema):
    id: UUID
    name: str
    start_date: date
    end_date: date
