from datetime import date
from typing import Optional
from uuid import UUID

from ninja import Schema


class UpdateTaskSchema(Schema):
    title: str
    description: str
    estimation: int
    completed: bool
    category: str
    parent_task_id: Optional[UUID]
    sprint_id: Optional[UUID]
    project_id: Optional[UUID]
    user_id: Optional[UUID]