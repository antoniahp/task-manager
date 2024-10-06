from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_status_column.create_status_column_command import CreateStatusColumnCommand
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.status_column.status_column_creator import StatusColumnCreator
from task_manager.domain.status_column.status_column_repository import StatusColumnRepository
from task_manager.domain.user.user_repository import UserRepository


class CreateStatusColumnCommandHandler(CommandHandler):
    def __init__(self, status_column_repository: StatusColumnRepository,
                 status_column_creator: StatusColumnCreator,
                 user_repository: UserRepository):
        self.__status_column_repository = status_column_repository
        self.__status_column_creator = status_column_creator
        self.__user_repository = user_repository

    def handle(self, command: CreateStatusColumnCommand) -> None:
        requester_user = self.__user_repository.filter_user_by_id(user_id=command.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=command.requester_user_id)

        if not requester_user.belongs_to_company(company_id=command.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=command.requester_user_id, company_id=command.company_id)

        column = self.__status_column_creator.status_column_creator(
            status_column_id=command.status_column_id,
            name=command.name,
            company_id=command.company_id,
            order=command.order
        )

        self.__status_column_repository.save_status_column(column)