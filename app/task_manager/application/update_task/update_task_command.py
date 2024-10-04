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
    parent_task_id: Optional[UUID]
    sprint_id: Optional[UUID]
    project_id: Optional[UUID]
    user_id: Optional[UUID]
    status_column_id: Optional[UUID]