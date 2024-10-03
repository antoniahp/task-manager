from typing import Optional
from uuid import UUID
from ninja import Schema

class CreateTaskSchema(Schema):
    title: str
    description: str
    estimation: int
    completed: bool
    category: str
    parent_task: Optional[UUID] = None
    sprint: Optional[UUID] = None
    project: Optional[UUID] = None
    user: Optional[UUID] = None