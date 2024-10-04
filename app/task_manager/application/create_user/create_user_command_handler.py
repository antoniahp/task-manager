from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_user.create_user_command import CreateUserCommand
from task_manager.domain.user.user_creator import UserCreator
from task_manager.domain.user.user_repository import UserRepository


class CreateUserCommandHandler(CommandHandler):
    def __init__(self, user_repository: UserRepository, user_creator: UserCreator):
        self.user_repository = user_repository
        self.user_creator = user_creator

    def handle(self, command: CreateUserCommand):
        user = self.user_creator.create_user(
            user_id=command.user_id,
            name=command.name,
            company_id=command.company,
            email=command.email,
            password=command.password,
            username=command.username
        )
        self.user_repository.save_user(user)
