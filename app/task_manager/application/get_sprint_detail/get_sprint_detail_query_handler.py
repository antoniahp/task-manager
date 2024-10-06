from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_sprint_detail.get_sprint_detail_query import GetSprintDetailQuery
from task_manager.domain.sprint.sprint_repository import SprintRepository
from task_manager.domain.sprint_detail.sprint_detail_creator import SprintDetailCreator
from task_manager.domain.task.task_repository import TaskRepository


class GetSprintDetailQueryHandler(QueryHandler):
    def __init__(self, task_repository: TaskRepository, sprint_repository: SprintRepository, sprint_detail_creator: SprintDetailCreator):
        self.__task_repository = task_repository
        self.__sprint_repository = sprint_repository
        self.__sprint_detail_creator = sprint_detail_creator

    def handle(self, query: GetSprintDetailQuery):
        sprint = self.__sprint_repository.filter_sprint_by_id(sprint_id=query.sprint_id)
        tasks = self.__task_repository.filter_task(sprint_id=query.sprint_id, completed=True)
        sprint_detail = self.__sprint_detail_creator.create(
            tasks=tasks,
            sprint=sprint,
        )
        return QueryResponse(content=sprint_detail)
