from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetUserQuery(Query):
    user_id: Optional[UUID] = None
    name: Optional[str] = None
    company_id: Optional[UUID] = None
