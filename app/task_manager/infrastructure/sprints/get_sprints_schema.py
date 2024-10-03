from datetime import date
from uuid import UUID

from ninja import Schema


class GetSprintsSchema(Schema):
    id: UUID
    name: str
    objective: str
    start_date: date
    end_date: date
    active: bool