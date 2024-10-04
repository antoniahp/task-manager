from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_task.get_task_query import GetTaskQuery
from task_manager.domain.task.task_repository import TaskRepository


class GetTaskQueryHandler(QueryHandler):
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    def handle(self, query: GetTaskQuery) -> QueryResponse:
        tasks = self._task_repository.filter_task(task_id=query.task_id, title=query.title, estimation=query.estimation, completed=query.completed, category=query.category, sprint_id=query.sprint, user_id=query.user, status_column_id=query.status_column_id, parent_task_id=query.parent_task, completed_at=query.completed_at, completed_at__lte=query.completed_at__lte, completed_at__gte=query.completed_at__gte)
        return QueryResponse(content=tasks)