from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_user_story.get_user_story_query import GetUserStoryQuery
from task_manager.domain.user_story.user_story_repository import UserStoryRepository


class GetUserStoryQueryHandler(QueryHandler):
    def __init__(self, user_story_repository: UserStoryRepository):
        self.__user_story_repository = user_story_repository

    def handle(self, query: GetUserStoryQuery) -> QueryResponse:
        tasks = self.__user_story_repository.filter_user_story(user_story_id=query.user_story_id, title=query.title, estimation=query.estimation, completed=query.completed, project_id=query.project_id, assigned_user_id=query.assigned_user_id, status_column_id=query.status_column_id, completed_at=query.completed_at, completed_at__lte=query.completed_at__lte, completed_at__gte=query.completed_at__gte)
        return QueryResponse(content=tasks)