from datetime import datetime
from typing import Optional
from uuid import UUID
from ninja import Schema

class CreateUserStorySchema(Schema):
    title: str
    description: str
    estimation: int
    completed: bool
    completed_at: Optional[datetime]
    project_id: Optional[UUID]
    assigned_user_id: Optional[UUID]
    status_column_id: Optional[UUID]