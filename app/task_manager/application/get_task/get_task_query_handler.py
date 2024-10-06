from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_task.get_task_query import GetTaskQuery
from task_manager.domain.task.task_repository import TaskRepository


class GetTaskQueryHandler(QueryHandler):
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    def handle(self, query: GetTaskQuery) -> QueryResponse:
        tasks = self._task_repository.filter_task(task_id=query.task_id, title=query.title, estimation=query.estimation, completed=query.completed, sprint_id=query.sprint, assigned_user_id=query.assigned_user_id, status_column_id=query.status_column_id, user_story_id=query.user_story_id, completed_at=query.completed_at, completed_at__lte=query.completed_at__lte, completed_at__gte=query.completed_at__gte, deleted=query.deleted)
        return QueryResponse(content=tasks)