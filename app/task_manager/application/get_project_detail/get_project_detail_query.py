from dataclasses import dataclass
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetProjectDetailQuery(Query):
    company_id: UUID
    requester_user_id: UUID
    project_id: UUID