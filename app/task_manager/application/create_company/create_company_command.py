from dataclasses import dataclass
from uuid import UUID

from cqrs.commands.command import Command

@dataclass(frozen=True)
class CreateCompanyCommand(Command):
    company_id: UUID
    name: str