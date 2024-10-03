from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetTaskQuery(Query):
    task_id: UUID
    title: str
    description: str
    estimation: int
    completed: bool
    category: str
    parent_task: Optional[UUID] = None
    sprint: Optional[UUID] = None
    project: Optional[UUID] = None
    user: Optional[UUID] = None