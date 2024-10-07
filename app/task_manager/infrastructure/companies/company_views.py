from typing import List, Optional
from uuid import UUID, uuid4

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from task_manager.application.create_company.create_company_command import CreateCompanyCommand
from task_manager.application.create_company.create_company_command_handler import CreateCompanyCommandHandler
from task_manager.application.get_company.get_company_query import GetCompanyQuery
from task_manager.application.get_company.get_company_query_handler import GetCompanyQueryHandler
from task_manager.domain.company.company_creator import CompanyCreator
from task_manager.domain.exceptions.company_not_found_exception import CompanyNotFoundException
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.infrastructure.companies.create_company_schema import CreateCompanySchema
from task_manager.infrastructure.companies.db_company_repository import DbCompanyRepository
from task_manager.infrastructure.companies.get_company_schema import GetCompanySchema
from task_manager.infrastructure.error_message_schema import ErrorMessageSchema
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.users.db_user_repository import DbUserRepository

company_router = Router(tags=["company"])

db_company_repository = DbCompanyRepository()
db_user_repository = DbUserRepository()
company_creator = CompanyCreator()
get_company_query_handler = GetCompanyQueryHandler(company_repository=db_company_repository, user_repository=db_user_repository)
create_company_command_handler = CreateCompanyCommandHandler(company_repository=db_company_repository, company_creator=company_creator)

@company_router.post("/", response={200: IdentifierSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def create_company(request, create_company_schema: CreateCompanySchema):
    id = uuid4()
    command = CreateCompanyCommand(
        company_id=id,
        name=create_company_schema.name,
    )
    create_company_command_handler.handle(command)
    return IdentifierSchema(id=id)

@company_router.get("/", response={200: List[GetCompanySchema], 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_companies_by_user(request, name: Optional[str] = None):
    query = GetCompanyQuery(
        name=name,
        requester_user_id=request.user.id,
    )
    try:
        query_response = get_company_query_handler.handle(query)
        companies = query_response.content

        return companies
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@company_router.get("/{company_id}", response={200: GetCompanySchema, 403: ErrorMessageSchema, 404: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_company_by_id(request, company_id: UUID):
    query = GetCompanyQuery(
        company_id=company_id,
        requester_user_id=request.user.id,
    )
    try:
        query_response = get_company_query_handler.handle(query)
        companies = query_response.content
        if len(companies) == 0:
            return 404, {"error": "Company not found"}
        return 200, companies[0]
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except CompanyNotFoundException as exception:
        return 404, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}

