from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_user.create_user_command import CreateUserCommand
from task_manager.domain.company.company_repository import CompanyRepository
from task_manager.domain.user.user_creator import UserCreator
from task_manager.domain.user.user_repository import UserRepository


class CreateUserCommandHandler(CommandHandler):
    def __init__(self, user_repository: UserRepository, user_creator: UserCreator, company_repository: CompanyRepository):
        self.user_repository = user_repository
        self.company_repository = company_repository
        self.user_creator = user_creator

    def handle(self, command: CreateUserCommand) -> None:
        company = None
        if command.company_id is not None:
            company = self.company_repository.filter_company_by_id(command.company_id)

        user = self.user_creator.create_user(
            user_id=command.user_id,
            name=command.name,
            email=command.email,
            password=command.password,
            username=command.username
        )
        self.user_repository.save_user(user=user, company=company)
