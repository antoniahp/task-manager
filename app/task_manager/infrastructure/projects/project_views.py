from datetime import date
from typing import Optional, List
from uuid import uuid4, UUID

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from task_manager.application.create_project.create_project_command import CreateProjectCommand
from task_manager.application.create_project.create_project_command_handler import CreateProjectCommandHandler
from task_manager.application.get_project.get_project_query import GetProjectQuery
from task_manager.application.get_project.get_project_query_handler import GetProjectQueryHandler
from task_manager.application.get_project_detail.get_project_detail_query import GetProjectDetailQuery
from task_manager.application.get_project_detail.get_project_detail_query_handler import GetProjectDetailQueryHandler
from task_manager.domain.exceptions.project_not_found_exception import ProjectNotFoundException
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.project.project_creator import ProjectCreator
from task_manager.domain.project_detail.project_detail_creator import ProjectDetailCreator
from task_manager.infrastructure.error_message_schema import ErrorMessageSchema
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.projects.create_project_schema import CreateProjectSchema
from task_manager.infrastructure.projects.db_project_repository import DbProjectRepository
from task_manager.infrastructure.projects.get_project_detail_schema import GetProjectDetailSchema
from task_manager.infrastructure.projects.get_project_schema import GetProjectSchema
from task_manager.infrastructure.task.db_task_repository import DbTaskRepository
from task_manager.infrastructure.users.db_user_repository import DbUserRepository

project_router = Router(tags=["projects"])

project_detail_creator = ProjectDetailCreator()
task_repository =DbTaskRepository()
project_repository = DbProjectRepository()
project_creator = ProjectCreator()
user_repository = DbUserRepository()
create_sprint_command_handler = CreateProjectCommandHandler(project_repository=project_repository, project_creator=project_creator, user_repository=user_repository)
get_project_query_handler = GetProjectQueryHandler(project_repository=project_repository, user_repository=user_repository)
get_project_detail_query_handler = GetProjectDetailQueryHandler(project_repository=project_repository, task_repository=task_repository, project_detail_creator=project_detail_creator, user_repository=user_repository)

@project_router.post("/", response={200: IdentifierSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def create_project(request, company_id: UUID, create_project_schema: CreateProjectSchema):
    id = uuid4()
    command = CreateProjectCommand(
        project_id=id,
        name=create_project_schema.name,
        start_date=create_project_schema.start_date,
        end_date=create_project_schema.end_date,
        company_id=company_id,
        requester_user_id=request.user.id,
    )
    try:
        create_sprint_command_handler.handle(command)
        return IdentifierSchema(id=id)
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@project_router.get("/", response={200:List[GetProjectSchema], 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_projects(request, company_id: UUID, name: Optional[str] = None, start_date__gte: Optional[date] = None, end_date__lte: Optional[date] = None):
    query = GetProjectQuery(
        name=name,
        start_date__gte=start_date__gte,
        end_date__lte=end_date__lte,
        company_id=company_id,
        requester_user_id=request.user.id,
    )
    try:
        query_response = get_project_query_handler.handle(query)
        projects = query_response.content
        return projects
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}

@project_router.get("/{project_id}", response={200: GetProjectSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_project_by_id(request, company_id: UUID, project_id: UUID):
    query = GetProjectQuery(
        project_id=project_id,
        company_id=company_id,
        requester_user_id=request.user.id
    )
    try:
        query_response = get_project_query_handler.handle(query)
        projects = query_response.content
        return projects[0]
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@project_router.get("/{project_id}/detail", response={200:GetProjectDetailSchema, 403: ErrorMessageSchema,404: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_project_detail(request, company_id: UUID, project_id: UUID):
    query = GetProjectDetailQuery(
        project_id=project_id,
        company_id=company_id,
        requester_user_id=request.user.id
    )
    try:
        query_response = get_project_detail_query_handler.handle(query)
        project_detail = query_response.content
        return project_detail
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except ProjectNotFoundException as exception:
        return 404, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}