from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_project.create_project_command import CreateProjectCommand
from task_manager.domain.project.project_creator import ProjectCreator
from task_manager.domain.project.project_repository import ProjectRepository



class CreateProjectCommandHandler(CommandHandler):
    def __init__(self, project_creator: ProjectCreator, project_repository: ProjectRepository):
        self.__project_creator = project_creator
        self.__project_repository = project_repository

    def handle(self, command: CreateProjectCommand):
        project = self.__project_creator.create_project(
            project_id=command.project_id,
            name=command.name,
            start_date=command.start_date,
            end_date=command.end_date,

        )
        self.__project_repository.save_project(project)