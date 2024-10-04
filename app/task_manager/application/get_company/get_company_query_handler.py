from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_company.get_company_query import GetCompanyQuery
from task_manager.domain.company.company_repository import CompanyRepository


class GetCompanyQueryHandler(QueryHandler):
    def __init__(self, company_repository: CompanyRepository):
        self.__company_repository = company_repository

    def handle(self, query: GetCompanyQuery):
        company = self.__company_repository.filter_company(company_id=query.company_id, name=query.name)
        return QueryResponse(content=company)
