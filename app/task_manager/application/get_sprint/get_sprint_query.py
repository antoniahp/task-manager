from dataclasses import dataclass
from datetime import date
from uuid import UUID

from cqrs.queries.query import Query


@dataclass
class GetSprintQuery(Query):
    sprint_id: UUID
    name: str
    objective: str
    start_date: date
    end_date: date
    active: bool