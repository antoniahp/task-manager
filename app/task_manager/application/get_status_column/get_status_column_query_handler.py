from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_status_column.get_status_column_query import GetStatusColumnQuery
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.status_column.status_column_repository import StatusColumnRepository
from task_manager.domain.user.user_repository import UserRepository


class GetStatusColumnQueryHandler(QueryHandler):
    def __init__(self, status_column_repository: StatusColumnRepository, user_repository: UserRepository):
        self.__status_column_repository = status_column_repository
        self.__user_repository = user_repository

    def handle(self, query: GetStatusColumnQuery) -> QueryResponse:
        requester_user = self.__user_repository.filter_user_by_id(user_id=query.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=query.requester_user_id)

        if not requester_user.belongs_to_company(company_id=query.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=query.requester_user_id, company_id=query.company_id)

        status_columns = self.__status_column_repository.filter_status_columns(
            status_column_id=query.status_column_id,
            name=query.name,
            company_id=query.company_id
        )
        return QueryResponse(content=status_columns)