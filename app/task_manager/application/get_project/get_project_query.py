from dataclasses import dataclass
from datetime import date
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetProjectQuery(Query):
    name: str
    start_date__gte: date
    end_date__lte: date