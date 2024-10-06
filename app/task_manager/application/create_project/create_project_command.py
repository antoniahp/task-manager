from dataclasses import dataclass
from datetime import date
from uuid import UUID

from cqrs.commands.command import Command


@dataclass(frozen=True)
class CreateProjectCommand(Command):
    company_id: UUID
    requester_user_id: UUID
    project_id: UUID
    name: str
    start_date: date
    end_date: date

