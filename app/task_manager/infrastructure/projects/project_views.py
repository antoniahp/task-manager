from datetime import date
from typing import Optional, List
from uuid import uuid4, UUID

from ninja import Router

from task_manager.application.create_project.create_project_command import CreateProjectCommand
from task_manager.application.create_project.create_project_command_handler import CreateProjectCommandHandler
from task_manager.application.get_project.get_project_query import GetProjectQuery
from task_manager.application.get_project.get_project_query_handler import GetProjectQueryHandler
from task_manager.domain.project.project_creator import ProjectCreator
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.projects.create_project_schema import CreateProjectSchema
from task_manager.infrastructure.projects.db_project_repository import DbProjectRepository
from task_manager.infrastructure.projects.get_project_schema import GetProjectSchema

project_router = Router(tags=["projects"])

project_repository = DbProjectRepository()
project_creator = ProjectCreator()
create_sprint_command_handler = CreateProjectCommandHandler(project_repository=project_repository, project_creator=project_creator)
get_project_query_handler = GetProjectQueryHandler(project_repository=project_repository)

@project_router.post("/project", response=IdentifierSchema)
def post_project(request, create_project_schema: CreateProjectSchema):
    id = uuid4()
    command = CreateProjectCommand(
        project_id=id,
        name=create_project_schema.name,
        start_date=create_project_schema.start_date,
        end_date=create_project_schema.end_date,
    )
    create_sprint_command_handler.handle(command)
    return IdentifierSchema(id=id)


@project_router.get("/project", response=List[GetProjectSchema])
def get_projects(request, name: Optional[str] = None, start_date__gte: Optional[date] = None, end_date__lte: Optional[date] = None):
    query = GetProjectQuery(
        name=name,
        start_date__gte=start_date__gte,
        end_date__lte=end_date__lte,
    )

    query_response = get_project_query_handler.handle(query)
    projects = query_response.content
    return projects

@project_router.get("/project/{project_id}", response=GetProjectSchema)
def get_project_by_id(request, project_id: UUID):
    query = GetProjectQuery(
        project_id=project_id,
    )

    query_response = get_project_query_handler.handle(query)
    projects = query_response.content
    return projects[0]
