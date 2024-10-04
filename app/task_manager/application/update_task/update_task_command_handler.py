from cqrs.commands.command_handler import CommandHandler
from task_manager.application.update_task.update_task_command import UpdateTaskCommand
from task_manager.domain.task.task_repository import TaskRepository


class UpdateTaskCommandHandler(CommandHandler):
    def __init__(self, task_repository:TaskRepository):
        self.__task_repository = task_repository

    def handle(self, command: UpdateTaskCommand):
        task_filtered = self.__task_repository.filter_task_by_id(task_id=command.task_id)
        task_filtered.title = command.title
        task_filtered.description = command.description
        task_filtered.estimation = command.estimation
        task_filtered.completed = command.completed
        task_filtered.category = command.category
        task_filtered.parent_task_id= command.parent_task_id
        task_filtered.sprint_id= command.sprint_id
        task_filtered.project_id= command.project_id
        task_filtered.user_id= command.user_id
        task_filtered.status_column_id= command.status_column_id

        self.__task_repository.save_task(task_filtered)
