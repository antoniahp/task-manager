from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_sprint.get_sprint_query import GetSprintQuery
from task_manager.domain.sprint.sprint_repository import SprintRepository


class GetSprintQueryHandler(QueryHandler):
    def __init__(self, sprint_repository: SprintRepository):
        self.__sprint_repository = sprint_repository

    def handle(self, query: GetSprintQuery) -> QueryResponse:
        sprints = self.__sprint_repository.filter_sprint(sprint_id=query.sprint_id, name=query.name, start_date=query.start_date, end_date=query.end_date, objective=query.objective,active=query.active)
        return QueryResponse(content=sprints)