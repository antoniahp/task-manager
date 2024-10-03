from dataclasses import dataclass
from datetime import date
from uuid import UUID

from cqrs.commands.command import Command


@dataclass(frozen=True)
class UpdateSprintCommand(Command):
    sprint_id: UUID
    name: str
    objective: str
    start_date: date
    end_date: date
    active: bool