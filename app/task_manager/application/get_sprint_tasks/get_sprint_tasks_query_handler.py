from uuid import UUID

from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_sprint_tasks.get_sprint_tasks_query import GetSprintTasksQuery
from task_manager.domain.sprint.sprint_repository import SprintRepository
from task_manager.domain.sprint_tasks.sprint_tasks_creator import SprintTasksCreator
from task_manager.domain.status_column.status_column_repository import StatusColumnRepository
from task_manager.domain.task.task_repository import TaskRepository


class GetSprintTasksQueryHandler(QueryHandler):
    def __init__(self, task_repository: TaskRepository, status_column_repository: StatusColumnRepository, sprint_repository: SprintRepository, sprint_tasks_creator: SprintTasksCreator):
        self.__task_repository = task_repository
        self.__status_column_repository = status_column_repository
        self.__sprint_repository = sprint_repository
        self.__sprint_tasks_creator = sprint_tasks_creator


    def handle(self, query: GetSprintTasksQuery) -> QueryResponse:
        sprint = self.__sprint_repository.filter_sprint_by_id(sprint_id=query.sprint_id)
        tasks = self.__task_repository.filter_task(sprint_id=query.sprint_id)
        company_columns = self.__status_column_repository.filter_status_columns(company_id=UUID(str(sprint.company_id)))
        sprint_tasks = self.__sprint_tasks_creator.create(
            tasks=tasks,
            columns=company_columns
        )
        return QueryResponse(content=sprint_tasks)
