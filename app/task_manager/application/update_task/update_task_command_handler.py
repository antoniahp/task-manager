from datetime import datetime

from cqrs.commands.command_handler import CommandHandler
from task_manager.application.update_task.update_task_command import UpdateTaskCommand
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.task.task_repository import TaskRepository
from task_manager.domain.exceptions.task_not_found_exception import TaskNotFoundException
from task_manager.domain.user.user_repository import UserRepository


class UpdateTaskCommandHandler(CommandHandler):
    def __init__(self, task_repository:TaskRepository, user_repository: UserRepository):
        self.__task_repository = task_repository
        self.__user_repository = user_repository

    def handle(self, command: UpdateTaskCommand) -> None:
        requester_user = self.__user_repository.filter_user_by_id(user_id=command.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=command.requester_user_id)

        if not requester_user.belongs_to_company(company_id=command.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=command.requester_user_id, company_id=command.company_id)

        task_filtered = self.__task_repository.filter_task_by_id(task_id=command.task_id)
        if task_filtered is None:
            raise TaskNotFoundException(task_id=command.task_id)

        task_filtered.title = command.title
        task_filtered.description = command.description
        task_filtered.estimation = command.estimation
        task_filtered.user_story_id= command.user_story_id
        task_filtered.sprint_id= command.sprint_id
        task_filtered.assigned_user_id= command.assigned_user_id
        task_filtered.status_column_id= command.status_column_id
        task_filtered.deleted = command.deleted
        if command.completed == True and task_filtered.completed == False:
            task_filtered.completed_at = datetime.now()
            task_filtered.completed= command.completed

        self.__task_repository.save_task(task_filtered)
