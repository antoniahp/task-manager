from datetime import date
from typing import List, Optional
from uuid import uuid4, UUID

from ninja_jwt.authentication import JWTAuth

from task_manager.application.create_sprint.create_sprint_command import CreateSprintCommand
from task_manager.application.create_sprint.create_sprint_command_handler import CreateSprintCommandHandler
from task_manager.application.get_sprint.get_sprint_query import GetSprintQuery
from task_manager.application.get_sprint.get_sprint_query_handler import GetSprintQueryHandler
from task_manager.application.get_sprint_detail.get_sprint_detail_query import GetSprintDetailQuery
from task_manager.application.get_sprint_detail.get_sprint_detail_query_handler import GetSprintDetailQueryHandler
from task_manager.application.get_sprint_tasks.get_sprint_tasks_query import GetSprintTasksQuery
from task_manager.application.get_sprint_tasks.get_sprint_tasks_query_handler import GetSprintTasksQueryHandler
from task_manager.application.update_sprint.update_sprint_command import UpdateSprintCommand
from task_manager.application.update_sprint.update_sprint_command_handler import UpdateSprintCommandHandler
from task_manager.domain.exceptions.sprint_not_found_exception import SprintNotFoundException
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.sprint.sprint_creator import SprintCreator
from task_manager.domain.sprint_detail.sprint_detail_creator import SprintDetailCreator
from task_manager.domain.sprint_tasks.sprint_tasks_creator import SprintTasksCreator
from task_manager.infrastructure.error_message_schema import ErrorMessageSchema
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.sprints.create_sprint_schema import CreateSprintSchema
from task_manager.infrastructure.sprints.db_sprint_repository import DbSprintRepository
from ninja import Router

from task_manager.infrastructure.sprints.get_sprint_detail_schema import GetSprintDetailSchema
from task_manager.infrastructure.sprints.get_sprints_schema import GetSprintsSchema
from task_manager.infrastructure.sprints.sprint_tasks_column_schema import SprintTasksColumnSchema
from task_manager.infrastructure.sprints.update_sprint_schema import UpdateSprintSchema
from task_manager.infrastructure.status_columns.db_status_column_repository import DbStatusColumnRepository
from task_manager.infrastructure.task.db_task_repository import DbTaskRepository
from task_manager.infrastructure.users.db_user_repository import DbUserRepository

sprint_router = Router(tags=['sprints'])

sprint_repository = DbSprintRepository()
sprint_creator = SprintCreator()


sprint_detail_creator = SprintDetailCreator()
sprint_tasks_creator = SprintTasksCreator()
status_column_repository = DbStatusColumnRepository()
user_repository = DbUserRepository()
task_repository = DbTaskRepository()
create_sprint_command_handler = CreateSprintCommandHandler(sprint_repository=sprint_repository, sprint_creator=sprint_creator, user_repository=user_repository)
get_sprint_query_handler = GetSprintQueryHandler(sprint_repository=sprint_repository, user_repository=user_repository)
update_sprint_command_handler = UpdateSprintCommandHandler(sprint_repository=sprint_repository, user_repository=user_repository)
get_sprint_tasks_query_handler = GetSprintTasksQueryHandler(sprint_repository=sprint_repository, status_column_repository=status_column_repository, sprint_tasks_creator=sprint_tasks_creator, task_repository=task_repository, user_repository=user_repository)
get_sprint_detail_query_handler = GetSprintDetailQueryHandler(sprint_repository=sprint_repository, task_repository=task_repository, sprint_detail_creator=sprint_detail_creator, user_repository=user_repository)
@sprint_router.post("/", response={200: IdentifierSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def create_sprint(request, company_id: UUID, create_sprint_schema: CreateSprintSchema):
    id = uuid4()
    command = CreateSprintCommand(
        sprint_id=id,
        name=create_sprint_schema.name,
        objective=create_sprint_schema.objective,
        start_date=create_sprint_schema.start_date,
        end_date=create_sprint_schema.end_date,
        active=create_sprint_schema.active,
        company_id=company_id,
        requester_user_id=request.user.id

    )
    try:
        create_sprint_command_handler.handle(command)
        return IdentifierSchema(id=id)
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@sprint_router.get("/", response={200: List[GetSprintsSchema], 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_sprints(request, company_id: UUID, sprint_id: Optional[UUID] = None, name: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None, objective: Optional[str] = None, active: Optional[bool] = None):
    query = GetSprintQuery(
        sprint_id=sprint_id,
        name=name,
        objective=objective,
        start_date=start_date,
        end_date=end_date,
        active=active,
        company_id=company_id,
        requester_user_id=request.user.id
    )
    try:
        query_response = get_sprint_query_handler.handle(query)
        sprints = query_response.content
        return sprints
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@sprint_router.get("/{sprint_id}", response={200: GetSprintsSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_sprint_by_id(request, company_id: UUID, sprint_id: UUID ):
    query = GetSprintQuery(
        sprint_id=sprint_id,
        company_id=company_id,
        requester_user_id=request.user.id
    )
    try:
        query_response = get_sprint_query_handler.handle(query)
        sprint = query_response.content
        return sprint[0]
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@sprint_router.get("/{sprint_id}/tasks", response={200: List[SprintTasksColumnSchema], 403: ErrorMessageSchema, 404:ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_sprint_tasks_by_columns(request, company_id: UUID, sprint_id: UUID):
    query = GetSprintTasksQuery(
        sprint_id=sprint_id,
        company_id = company_id,
        requester_user_id = request.user.id
    )
    try:
        query_response = get_sprint_tasks_query_handler.handle(query)
        sprint_tasks = query_response.content
        return sprint_tasks.columns
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except SprintNotFoundException as exception:
        return 404, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@sprint_router.get("/{sprint_id}/detail", response={200:GetSprintDetailSchema, 403: ErrorMessageSchema, 404:ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_sprint_detail(request, company_id: UUID, sprint_id: UUID):
    query = GetSprintDetailQuery(
        sprint_id=sprint_id,
        company_id=company_id,
        requester_user_id=request.user.id
    )
    try:
        query_response = get_sprint_detail_query_handler.handle(query)
        sprint_detail = query_response.content
        return sprint_detail
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except SprintNotFoundException as exception:
        return 404, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@sprint_router.put("/{sprint_id}", response={200: None, 403: ErrorMessageSchema, 404: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def update_sprint(request, company_id: UUID, sprint_id: UUID, update_schema: UpdateSprintSchema):
    command = UpdateSprintCommand(
        sprint_id=sprint_id,
        name=update_schema.name,
        objective=update_schema.objective,
        start_date=update_schema.start_date,
        end_date=update_schema.end_date,
        active=update_schema.active,
        company_id=company_id,
        requester_user_id=request.user.id
    )
    try:
        update_sprint_command_handler.handle(command)
        return {"success": True}
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except SprintNotFoundException as exception:
        return 404, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}
