from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from cqrs.queries.query import Query

@dataclass(frozen=True)
class GetStatusColumnQuery(Query):
    company_id: UUID
    requester_user_id: UUID
    status_column_id: Optional[UUID] = None
    name:  Optional[str] = None
