from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from cqrs.queries.query import Query


@dataclass(frozen=True)
class GetTaskQuery(Query):
    task_id: Optional[UUID] = None
    title: Optional[str]= None
    description: Optional[str]= None
    estimation: Optional[int]= None
    completed: Optional[bool]= None
    category: Optional[str]= None
    parent_task: Optional[UUID] = None
    sprint: Optional[UUID] = None
    project: Optional[UUID] = None
    user: Optional[UUID] = None