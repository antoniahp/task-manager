from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_project.get_project_query import GetProjectQuery
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.project.project_repository import ProjectRepository
from task_manager.domain.user.user_repository import UserRepository


class GetProjectQueryHandler(QueryHandler):
    def __init__(self, project_repository: ProjectRepository, user_repository:UserRepository):
        self.__project_repository = project_repository
        self.__user_repository = user_repository

    def handle(self, query: GetProjectQuery) -> QueryResponse:
        requester_user = self.__user_repository.filter_user_by_id(user_id=query.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=query.requester_user_id)

        if not requester_user.belongs_to_company(company_id=query.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=query.requester_user_id, company_id=query.company_id)

        projects = self.__project_repository.filtered_projects(project_id=query.project_id, name=query.name, start_date__gte=query.start_date__gte, end_date__lte=query.end_date__lte)
        return QueryResponse(content=projects)
