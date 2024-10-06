from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from cqrs.commands.command import Command


@dataclass(frozen=True)
class UpdateTaskCommand(Command):
    company_id: UUID
    requester_user_id: UUID
    task_id: UUID
    title:str
    description:str
    estimation: int
    completed: bool
    deleted: bool
    user_story_id: UUID
    sprint_id: Optional[UUID]
    assigned_user_id: Optional[UUID]
    status_column_id: Optional[UUID]