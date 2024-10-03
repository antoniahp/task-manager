from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_task.get_task_query import GetTaskQuery
from task_manager.domain.task.task_repository import TaskRepository


class GetTaskQueryHandler(QueryHandler):
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    def handle(self, query: GetTaskQuery) -> QueryResponse:
        tasks = self._task_repository.filter_task(task_id=query.task_id, title=query.title, estimation=query.estimation, completed=query.completed, category=query.category, sprint=query.sprint, user=query.user)
        return QueryResponse(content=tasks)