from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from cqrs.commands.command import Command


@dataclass(frozen=True)
class CreateUserStoryCommand(Command):
    company_id: UUID
    requester_user_id: UUID
    user_story_id: UUID
    title: str
    description: str
    estimation: int
    completed: bool
    completed_at: datetime
    project_id: UUID
    assigned_user_id: UUID
    status_column_id: UUID