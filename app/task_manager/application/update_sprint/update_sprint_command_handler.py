from cqrs.commands.command_handler import CommandHandler
from task_manager.application.update_sprint.update_sprint_command import UpdateSprintCommand
from task_manager.domain.sprint.sprint_repository import SprintRepository


class UpdateSprintCommandHandler(CommandHandler):
    def __init__(self, sprint_repository:SprintRepository):
        self.__sprint_repository = sprint_repository

    def handle(self, command: UpdateSprintCommand):
        sprint_filtered = self.__sprint_repository.filter_sprint_by_id(sprint_id=command.sprint_id)
        sprint_filtered.name = command.name
        sprint_filtered.objective = command.objective
        sprint_filtered.start_date = command.start_date
        sprint_filtered.end_date = command.end_date
        sprint_filtered.active = command.active

        self.__sprint_repository.save_sprint(sprint_filtered)
