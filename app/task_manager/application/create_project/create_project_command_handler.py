from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_project.create_project_command import CreateProjectCommand
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.project.project_creator import ProjectCreator
from task_manager.domain.project.project_repository import ProjectRepository
from task_manager.domain.user.user_repository import UserRepository


class CreateProjectCommandHandler(CommandHandler):
    def __init__(self, project_creator: ProjectCreator, project_repository: ProjectRepository, user_repository: UserRepository):
        self.__project_creator = project_creator
        self.__project_repository = project_repository
        self.__user_repository = user_repository

    def handle(self, command: CreateProjectCommand) -> None:
        requester_user = self.__user_repository.filter_user_by_id(user_id=command.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=command.requester_user_id)

        if not requester_user.belongs_to_company(company_id=command.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=command.requester_user_id, company_id=command.company_id)

        project = self.__project_creator.create_project(
            project_id=command.project_id,
            name=command.name,
            start_date=command.start_date,
            end_date=command.end_date,

        )
        self.__project_repository.save_project(project)