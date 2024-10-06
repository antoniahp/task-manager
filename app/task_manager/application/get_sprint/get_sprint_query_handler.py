from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_sprint.get_sprint_query import GetSprintQuery
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.sprint.sprint_repository import SprintRepository
from task_manager.domain.user.user_repository import UserRepository


class GetSprintQueryHandler(QueryHandler):
    def __init__(self, sprint_repository: SprintRepository, user_repository: UserRepository):
        self.__sprint_repository = sprint_repository
        self.__user_repository = user_repository

    def handle(self, query: GetSprintQuery) -> QueryResponse:
        requester_user = self.__user_repository.filter_user_by_id(user_id=query.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=query.requester_user_id)

        if not requester_user.belongs_to_company(company_id=query.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=query.requester_user_id, company_id=query.company_id)

        sprints = self.__sprint_repository.filter_sprint(
            sprint_id=query.sprint_id,
            name=query.name,
            start_date=query.start_date,
            end_date=query.end_date,
            objective=query.objective,
            active=query.active,
            company_id=query.company_id
        )
        return QueryResponse(content=sprints)