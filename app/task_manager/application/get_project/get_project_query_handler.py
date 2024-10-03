from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_project.get_project_query import GetProjectQuery
from task_manager.domain.project.project_repository import ProjectRepository


class GetProjectQueryHandler(QueryHandler):
    def __init__(self, project_repository: ProjectRepository):
        self.__project_repository = project_repository

    def handle(self, query: GetProjectQuery) -> QueryResponse:
        projects = self.__project_repository.filtered_projects(name=query.name, start_date__gte=query.start_date__gte, end_date__lte=query.end_date__lte)
        return QueryResponse(content=projects)
