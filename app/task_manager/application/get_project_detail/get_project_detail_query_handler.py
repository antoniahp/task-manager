from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_project_detail.get_project_detail_query import GetProjectDetailQuery
from task_manager.domain.project.project_repository import ProjectRepository
from task_manager.domain.project_detail.project_detail_creator import ProjectDetailCreator
from task_manager.domain.task.task_repository import TaskRepository


class GetProjectDetailQueryHandler(QueryHandler):
    def __init__(self, task_repository: TaskRepository, project_detail_creator: ProjectDetailCreator, project_repository: ProjectRepository):
        self.__task_repository = task_repository
        self.__project_detail_creator = project_detail_creator
        self.__project_repository = project_repository
    def handle(self, query: GetProjectDetailQuery) -> QueryResponse:
        project = self.__project_repository.filtered_project_by_id(project_id=query.project_id)
        project_tasks = self.__task_repository.filter_task(project_id=query.project_id)
        total_estimation_project = 0
        for project_task in project_tasks:
            total_estimation_project = project_task.estimation + total_estimation_project

        project_detail = self.__project_detail_creator.create(
            project=project,
            total_estimation_project=total_estimation_project
        )

        return QueryResponse(content=project_detail)