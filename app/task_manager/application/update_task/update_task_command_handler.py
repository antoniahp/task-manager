from cqrs.commands.command_handler import CommandHandler
from task_manager.application.update_task.update_task_command import UpdateTaskCommand
from task_manager.domain.task.task_repository import TaskRepository
from task_manager.infrastructure.exceptions.task_not_found_exception import TaskNotFoundException


class UpdateTaskCommandHandler(CommandHandler):
    def __init__(self, task_repository:TaskRepository):
        self.__task_repository = task_repository

    def handle(self, command: UpdateTaskCommand):
        task_filtered = self.__task_repository.filter_task_by_id(task_id=command.task_id)
        if task_filtered is None:
            raise TaskNotFoundException(task_id=command.task_id)

        task_filtered.title = command.title
        task_filtered.description = command.description
        task_filtered.estimation = command.estimation
        task_filtered.completed = command.completed
        task_filtered.user_story_id= command.user_story_id
        task_filtered.sprint_id= command.sprint_id
        task_filtered.assigned_user_id= command.assigned_user_id
        task_filtered.status_column_id= command.status_column_id

        self.__task_repository.save_task(task_filtered)
