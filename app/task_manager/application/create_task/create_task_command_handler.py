from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_task.create_task_command import CreateTaskCommand
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.task.task_creator import TaskCreator
from task_manager.domain.task.task_repository import TaskRepository
from task_manager.domain.user.user_repository import UserRepository


class CreateTaskCommandHandler(CommandHandler):
    def __init__(self, task_creator: TaskCreator, task_repository: TaskRepository, user_repository: UserRepository):
        self.__task_creator = task_creator
        self.__task_repository = task_repository
        self.__user_repository = user_repository


    def handle(self, command: CreateTaskCommand):
        requester_user = self.__user_repository.filter_user_by_id(user_id=command.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=command.requester_user_id)

        if not requester_user.belongs_to_company(company_id=command.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=command.requester_user_id, company_id=command.company_id)

        task = self.__task_creator.create_task(
            task_id=command.task_id,
            title=command.title,
            description=command.description,
            estimation=command.estimation,
            completed=command.completed,
            user_story_id=command.user_story_id,
            sprint_id=command.sprint_id,
            assigned_user_id=command.assigned_user_id,
            status_column_id=command.status_column_id,
            completed_at=command.completed_at,
            deleted=command.deleted
        )
        self.__task_repository.save_task(task)