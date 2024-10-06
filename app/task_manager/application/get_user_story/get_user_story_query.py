from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetUserStoryQuery(Query):
    company_id: UUID
    requester_user_id: UUID
    user_story_id: Optional[UUID] = None
    title: Optional[str]= None
    description: Optional[str]= None
    estimation: Optional[int]= None
    completed: Optional[bool]= None
    project_id: Optional[UUID] = None
    assigned_user_id: Optional[UUID] = None
    status_column_id: Optional[UUID] = None
    completed_at: Optional[datetime] =None
    completed_at__gte: Optional[datetime]= None
    completed_at__lte: Optional[datetime]= None
