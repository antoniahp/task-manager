from typing import Optional
from uuid import UUID
from ninja import Schema
from pydantic import Field


class CreateTaskSchema(Schema):
    title: str
    description: str
    estimation: int
    completed: bool
    deleted: bool = Field(default=False)
    user_story_id: UUID
    sprint_id: Optional[UUID]
    assigned_user_id: Optional[UUID]
    status_column_id: Optional[UUID]