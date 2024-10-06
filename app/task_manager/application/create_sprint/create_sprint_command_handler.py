from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_sprint.create_sprint_command import CreateSprintCommand
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.sprint.sprint_creator import SprintCreator
from task_manager.domain.sprint.sprint_repository import SprintRepository
from task_manager.domain.user.user_repository import UserRepository


class CreateSprintCommandHandler(CommandHandler):
    def __init__(self, sprint_creator: SprintCreator, sprint_repository: SprintRepository, user_repository: UserRepository ):
        self.__sprint_creator = sprint_creator
        self.__sprint_repository= sprint_repository
        self.__user_repository = user_repository

    def handle(self, command: CreateSprintCommand):
        requester_user = self.__user_repository.filter_user_by_id(user_id=command.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=command.requester_user_id)

        if not requester_user.belongs_to_company(company_id=command.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=command.requester_user_id, company_id=command.company_id)

        sprint = self.__sprint_creator.create_sprint(
            sprint_id=command.sprint_id,
            name=command.name,
            objective=command.objective,
            start_date=command.start_date,
            end_date=command.end_date,
            active=command.active
        )
        self.__sprint_repository.save_sprint(sprint)