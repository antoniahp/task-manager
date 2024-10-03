from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetSprintQuery(Query):
    sprint_id: Optional[UUID] = None
    name: Optional[str] = None
    objective: Optional[str] = None
    start_date:Optional[date] = None
    end_date: Optional[date] = None
    active:Optional[bool] = None