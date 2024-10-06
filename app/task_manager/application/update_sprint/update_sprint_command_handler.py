from cqrs.commands.command_handler import CommandHandler
from task_manager.application.update_sprint.update_sprint_command import UpdateSprintCommand
from task_manager.domain.exceptions.sprint_not_found_exception import SprintNotFoundException
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.sprint.sprint_repository import SprintRepository
from task_manager.domain.user.user_repository import UserRepository


class UpdateSprintCommandHandler(CommandHandler):
    def __init__(self, sprint_repository: SprintRepository, user_repository: UserRepository):
        self.__sprint_repository = sprint_repository
        self.__user_repository = user_repository

    def handle(self, command: UpdateSprintCommand) -> None:
        requester_user = self.__user_repository.filter_user_by_id(user_id=command.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=command.requester_user_id)

        if not requester_user.belongs_to_company(company_id=command.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=command.requester_user_id, company_id=command.company_id)

        sprint_filtered = self.__sprint_repository.filter_sprint_by_id(sprint_id=command.sprint_id)
        if sprint_filtered is None:
            raise SprintNotFoundException(sprint_id=command.sprint_id)

        sprint_filtered.name = command.name
        sprint_filtered.objective = command.objective
        sprint_filtered.start_date = command.start_date
        sprint_filtered.end_date = command.end_date
        sprint_filtered.active = command.active

        self.__sprint_repository.save_sprint(sprint_filtered)
