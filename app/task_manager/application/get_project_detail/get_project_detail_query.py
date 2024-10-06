from dataclasses import dataclass
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetProjectDetailQuery(Query):
    project_id: UUID