from dataclasses import dataclass
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetSprintDetailQuery(Query):
    company_id: UUID
    requester_user_id: UUID
    sprint_id: UUID
