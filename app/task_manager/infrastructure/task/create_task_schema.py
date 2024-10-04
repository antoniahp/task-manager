from typing import Optional
from uuid import UUID
from ninja import Schema

class CreateTaskSchema(Schema):
    title: str
    description: str
    estimation: int
    completed: bool
    category: str
    parent_task: Optional[UUID]
    sprint: Optional[UUID]
    project: Optional[UUID]
    user_id: Optional[UUID]
    status_column_id: Optional[UUID]