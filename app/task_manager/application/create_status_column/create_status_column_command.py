from dataclasses import dataclass
from uuid import UUID

from cqrs.commands.command import Command


@dataclass(frozen=True)
class CreateStatusColumnCommand(Command):
    status_column_id: UUID
    name: str
    order: int
    company_id: UUID
    requester_user_id: UUID