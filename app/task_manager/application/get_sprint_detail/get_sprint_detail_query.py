from dataclasses import dataclass
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetSprintDetailQuery(Query):
    sprint_id: UUID
