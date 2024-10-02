from abc import ABC, abstractmethod

from cqrs.commands.command import Command

class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command) -> None:
        pass