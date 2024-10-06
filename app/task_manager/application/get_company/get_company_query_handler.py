from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_company.get_company_query import GetCompanyQuery
from task_manager.domain.company.company_repository import CompanyRepository
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.user.user_repository import UserRepository


class GetCompanyQueryHandler(QueryHandler):
    def __init__(self, company_repository: CompanyRepository, user_repository: UserRepository):
        self.__company_repository = company_repository
        self.__user_repository = user_repository

    def handle(self, query: GetCompanyQuery) -> QueryResponse:
        requester_user = self.__user_repository.filter_user_by_id(user_id=query.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=query.requester_user_id)

        if not requester_user.belongs_to_company(company_id=query.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=query.requester_user_id, company_id=query.company_id)

        company = self.__company_repository.filter_company(company_id=query.company_id, name=query.name)
        return QueryResponse(content=company)
