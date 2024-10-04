from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_status_column.create_status_column_command import CreateStatusColumnCommand
from task_manager.domain.status_column.status_column_creator import StatusColumnCreator
from task_manager.domain.status_column.status_column_repository import StatusColumnRepository


class CreateStatusColumnCommandHandler(CommandHandler):
    def __init__(self, status_column_repository: StatusColumnRepository, status_column_creator: StatusColumnCreator):
        self.__status_column_repository = status_column_repository
        self.__status_column_creator = status_column_creator

    def handle(self, command: CreateStatusColumnCommand):
        column = self.__status_column_creator.status_column_creator(
            status_column_id=command.status_column_id,
            name=command.name,
            company_id=command.company_id
        )

        self.__status_column_repository.save_status_column(column)