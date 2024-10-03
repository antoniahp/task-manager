from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetProjectQuery(Query):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    start_date__gte: Optional[date] = None
    end_date__lte: Optional[date] = None