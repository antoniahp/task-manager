from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_status_column.get_status_column_query import GetStatusColumnQuery
from task_manager.domain.status_column.status_column_repository import StatusColumnRepository


class GetStatusColumnQueryHandler(QueryHandler):
    def __init__(self, status_column_repository: StatusColumnRepository):
        self.__status_column_repository = status_column_repository

    def handle(self, query: GetStatusColumnQuery) -> QueryResponse:
        status_columns = self.__status_column_repository.filter_status_columns(status_column_id=query.status_column_id, name=query.name, company_id=query.company_id, order=query.order)
        return QueryResponse(content=status_columns)