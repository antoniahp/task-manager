from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from cqrs.commands.command import Command


@dataclass(frozen=True)
class UpdateTaskCommand(Command):
    task_id: UUID
    title:str
    description:str
    estimation: int
    completed: bool
    category:str
    parent_task_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    user_id: Optional[UUID] = None