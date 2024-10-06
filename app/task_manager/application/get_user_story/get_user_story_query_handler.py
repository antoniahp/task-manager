from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_user_story.get_user_story_query import GetUserStoryQuery
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.user.user_repository import UserRepository
from task_manager.domain.user_story.user_story_repository import UserStoryRepository


class GetUserStoryQueryHandler(QueryHandler):
    def __init__(self, user_story_repository: UserStoryRepository, user_repository: UserRepository):
        self.__user_story_repository = user_story_repository
        self.__user_repository = user_repository

    def handle(self, query: GetUserStoryQuery) -> QueryResponse:
        requester_user = self.__user_repository.filter_user_by_id(user_id=query.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=query.requester_user_id)

        if not requester_user.belongs_to_company(company_id=query.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=query.requester_user_id, company_id=query.company_id)

        tasks = self.__user_story_repository.filter_user_story(user_story_id=query.user_story_id, title=query.title, estimation=query.estimation, completed=query.completed, project_id=query.project_id, assigned_user_id=query.assigned_user_id, status_column_id=query.status_column_id, completed_at=query.completed_at, completed_at__lte=query.completed_at__lte, completed_at__gte=query.completed_at__gte, company_id=query.company_id)
        return QueryResponse(content=tasks)