from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_user.get_user_query import GetUserQuery
from task_manager.domain.user.user_repository import UserRepository


class GetUserQueryHandler(QueryHandler):
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def handle(self, query: GetUserQuery) -> QueryResponse:
        users = self.__user_repository.filter_users(
            user_id=query.user_id,
            name=query.name,
            company=query.company
        )
        return QueryResponse(content=users)
