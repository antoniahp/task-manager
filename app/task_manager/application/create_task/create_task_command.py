from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from cqrs.commands.command import Command



@dataclass(frozen=True)
class CreateTaskCommand(Command):
    task_id: UUID
    title: str
    description: str
    estimation: int
    completed: bool
    completed_at: datetime
    user_story_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None
    assigned_user_id: Optional[UUID] = None
    status_column_id: Optional[UUID] = None
