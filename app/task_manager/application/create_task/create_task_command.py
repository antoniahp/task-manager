from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from cqrs.commands.command import Command



@dataclass(frozen=True)
class CreateTaskCommand(Command):
    requester_user_id: UUID
    company_id: UUID
    task_id: UUID
    title: str
    description: str
    estimation: int
    completed: bool
    deleted: bool
    completed_at: datetime
    user_story_id: UUID
    sprint_id: Optional[UUID] = None
    assigned_user_id: Optional[UUID] = None
    status_column_id: Optional[UUID] = None

