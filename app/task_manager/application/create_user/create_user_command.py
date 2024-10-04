from dataclasses import dataclass
from uuid import UUID

from cqrs.commands.command import Command


@dataclass(frozen=True)
class CreateUserCommand(Command):
    user_id: UUID
    name: str
    company_id: UUID
    username: str
    password: str
    email: str
