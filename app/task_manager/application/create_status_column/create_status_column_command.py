from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from cqrs.commands.command import Command


@dataclass(frozen=True)
class CreateStatusColumnCommand(Command):
    status_column_id: UUID
    name: str
    company_id: Optional[UUID] = None