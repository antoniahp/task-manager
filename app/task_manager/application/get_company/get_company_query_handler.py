from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_company.get_company_query import GetCompanyQuery
from task_manager.domain.company.company_repository import CompanyRepository
from task_manager.domain.exceptions.company_not_found_exception import CompanyNotFoundException
from task_manager.domain.user.user_repository import UserRepository


class GetCompanyQueryHandler(QueryHandler):
    def __init__(self, company_repository: CompanyRepository, user_repository: UserRepository):
        self.__company_repository = company_repository
        self.__user_repository = user_repository

    def handle(self, query: GetCompanyQuery) -> QueryResponse:
        company = self.__company_repository.filter_company(company_id=query.company_id, name=query.name, requester_user_id=query.requester_user_id)
        if company is None:
            raise CompanyNotFoundException(company_id=query.company_id)
        return QueryResponse(content=company)
