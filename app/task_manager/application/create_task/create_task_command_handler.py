from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_task.create_task_command import CreateTaskCommand
from task_manager.domain.task.task_creator import TaskCreator
from task_manager.domain.task.task_repository import TaskRepository


class CreateTaskCommandHandler(CommandHandler):
    def __init__(self, task_creator: TaskCreator, task_repository: TaskRepository):
        self.__task_creator = task_creator
        self.__task_repository = task_repository

    def handle(self, command: CreateTaskCommand):
        task = self.__task_creator.create_task(
            task_id=command.task_id,
            title=command.title,
            description=command.description,
            estimation=command.estimation,
            completed=command.completed,
            category=command.category,
            parent_task=command.parent_task,
            sprint=command.sprint,
            project=command.project,
            user=command.user
        )
        self.__task_repository.save_task(task)