from typing import Optional
from uuid import UUID

from ninja import Schema


class GetTaskSchema(Schema):
    task_id: UUID
    title: str
    description: str
    estimation: int
    completed: bool
    category: str
    parent_task: Optional[UUID]
    sprint: Optional[UUID]
    project: Optional[UUID]
    user: Optional[UUID]