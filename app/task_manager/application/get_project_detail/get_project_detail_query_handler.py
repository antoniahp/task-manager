from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_project_detail.get_project_detail_query import GetProjectDetailQuery
from task_manager.domain.exceptions.project_not_found_exception import ProjectNotFoundException
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.project.project_repository import ProjectRepository
from task_manager.domain.project_detail.project_detail_creator import ProjectDetailCreator
from task_manager.domain.task.task_repository import TaskRepository
from task_manager.domain.user.user_repository import UserRepository


class GetProjectDetailQueryHandler(QueryHandler):
    def __init__(self, task_repository: TaskRepository, project_detail_creator: ProjectDetailCreator, project_repository: ProjectRepository, user_repository:UserRepository):
        self.__task_repository = task_repository
        self.__project_detail_creator = project_detail_creator
        self.__project_repository = project_repository
        self.__user_repository =user_repository
    def handle(self, query: GetProjectDetailQuery) -> QueryResponse:
        requester_user = self.__user_repository.filter_user_by_id(user_id=query.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=query.requester_user_id)

        if not requester_user.belongs_to_company(company_id=query.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=query.requester_user_id, company_id=query.company_id)

        project = self.__project_repository.filtered_project_by_id(project_id=query.project_id)
        if project is None:
            raise ProjectNotFoundException(project_id=query.project_id)

        project_tasks = self.__task_repository.filter_task(project_id=query.project_id)

        total_estimation_project = 0
        for project_task in project_tasks:
            total_estimation_project = project_task.estimation + total_estimation_project

        project_detail = self.__project_detail_creator.create(
            project=project,
            total_estimation_project=total_estimation_project
        )

        return QueryResponse(content=project_detail)