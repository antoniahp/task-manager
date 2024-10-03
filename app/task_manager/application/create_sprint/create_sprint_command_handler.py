from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_sprint.create_sprint_command import CreateSprintCommand
from task_manager.domain.sprint.sprint_creator import SprintCreator
from task_manager.domain.sprint.sprint_repository import SprintRepository



class CreateSprintCommandHandler(CommandHandler):
    def __init__(self, sprint_creator: SprintCreator, sprint_repository: SprintRepository):
        self.__sprint_creator = sprint_creator
        self.__sprint_repository= sprint_repository

    def handle(self, command: CreateSprintCommand):
        sprint = self.__sprint_creator.create_sprint(
            sprint_id=command.sprint_id,
            name=command.name,
            objective=command.objective,
            start_date=command.start_date,
            end_date=command.end_date,
            active=command.active
        )
        self.__sprint_repository.save_sprint(sprint)