from typing import List, Optional
from uuid import UUID, uuid4

from ninja import Router

from task_manager.application.create_company.create_company_command import CreateCompanyCommand
from task_manager.application.create_company.create_company_command_handler import CreateCompanyCommandHandler
from task_manager.application.get_company.get_company_query import GetCompanyQuery
from task_manager.application.get_company.get_company_query_handler import GetCompanyQueryHandler
from task_manager.domain.company.company_creator import CompanyCreator
from task_manager.infrastructure.companies.create_company_schema import CreateCompanySchema
from task_manager.infrastructure.companies.db_company_repository import DbCompanyRepository
from task_manager.infrastructure.companies.get_company_schema import GetCompanySchema
from task_manager.infrastructure.identifier_schema import IdentifierSchema

company_router = Router(tags=["company"])

db_company_repository = DbCompanyRepository()
company_creator = CompanyCreator()
get_company_query_handler = GetCompanyQueryHandler(company_repository=db_company_repository)
create_company_command_handler = CreateCompanyCommandHandler(company_repository=db_company_repository, company_creator=company_creator)
@company_router.get("/company", response=List[GetCompanySchema])
def get_companies(request, company_id: Optional[UUID] = None, name: Optional[str] = None):
    query = GetCompanyQuery(
        company_id=company_id,
        name=name,
    )

    query_response = get_company_query_handler.handle(query)
    companies = query_response.content

    return companies


@company_router.get("/company/{company_id}", response=GetCompanySchema)
def get_sprints_by_id(request, company_id: UUID ):
    query = GetCompanyQuery(
        company_id=company_id
    )

    query_response = get_company_query_handler.handle(query)
    company = query_response.content
    return company

@company_router.post("/company", response=IdentifierSchema)
def post_company(request, create_company_schema: CreateCompanySchema):
    id = uuid4()
    command = CreateCompanyCommand(
        company_id=id,
        name=create_company_schema.name,
    )
    create_company_command_handler.handle(command)
    return IdentifierSchema(id=id)
