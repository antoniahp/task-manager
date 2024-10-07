from typing import List, Optional
from uuid import uuid4, UUID

from task_manager.application.create_task.create_task_command import CreateTaskCommand
from task_manager.application.create_task.create_task_command_handler import CreateTaskCommandHandler
from task_manager.application.get_task.get_task_query import GetTaskQuery
from task_manager.application.get_task.get_task_query_handler import GetTaskQueryHandler
from task_manager.application.update_task.update_task_command import UpdateTaskCommand
from task_manager.application.update_task.update_task_command_handler import UpdateTaskCommandHandler
from task_manager.domain.exceptions.task_not_found_exception import TaskNotFoundException
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.task.task_creator import TaskCreator
from task_manager.infrastructure.error_message_schema import ErrorMessageSchema
from task_manager.infrastructure.task.get_task_schema import GetTaskSchema
from task_manager.infrastructure.task.create_task_schema import CreateTaskSchema
from task_manager.infrastructure.task.db_task_repository import DbTaskRepository
from ninja import Router

from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.task.update_task_schema import UpdateTaskSchema
from ninja_jwt.authentication import JWTAuth

from task_manager.infrastructure.users.db_user_repository import DbUserRepository

task_router = Router(tags=["tasks"])

task_repository = DbTaskRepository()
task_creator = TaskCreator()
user_repository = DbUserRepository()
create_task_command_handler = CreateTaskCommandHandler(task_repository=task_repository, task_creator=task_creator, user_repository=user_repository)
get_task_query_handler = GetTaskQueryHandler(task_repository=task_repository, user_repository=user_repository)
update_task_command_handler = UpdateTaskCommandHandler(task_repository=task_repository, user_repository=user_repository)


@task_router.post("/", response={200: IdentifierSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def create_task(request, company_id: UUID, create_task_schema: CreateTaskSchema):
    id = uuid4()
    command = CreateTaskCommand(
        task_id=id,
        title=create_task_schema.title,
        description=create_task_schema.description,
        estimation=create_task_schema.estimation,
        completed=create_task_schema.completed,
        user_story_id=create_task_schema.user_story_id,
        sprint_id=create_task_schema.sprint_id,
        assigned_user_id=create_task_schema.assigned_user_id,
        status_column_id=create_task_schema.status_column_id,
        deleted=False,
        company_id=company_id,
        requester_user_id=request.user.id,

    )
    try:
        create_task_command_handler.handle(command)
        return IdentifierSchema(id=id)
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}



@task_router.get("/", response={200: List[GetTaskSchema], 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_tasks(request, company_id: UUID, title: Optional[str] = None,
             description: Optional[str] = None, estimation: Optional[int] = None,
             completed: Optional[bool] = None,
             user_story_id: Optional[UUID] = None, sprint: Optional[UUID] = None,
             assigned_user_id: Optional[UUID] = None, status_column_id: Optional[UUID] = None):
    query = GetTaskQuery(
        requester_user_id=request.user.id,
        company_id=company_id,
        title=title,
        description=description,
        estimation=estimation,
        completed=completed,
        user_story_id=user_story_id,
        sprint=sprint,
        assigned_user_id=assigned_user_id,
        status_column_id=status_column_id,
        deleted=False
    )
    try:
        query_response = get_task_query_handler.handle(query)
        tasks = query_response.content
        return 200, tasks
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}

@task_router.get("/{task_id}", response={200: GetTaskSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_task_by_id(request, company_id: UUID, task_id: UUID):
    query = GetTaskQuery(
        task_id=task_id,
        deleted=False,
        company_id=company_id,
        requester_user_id=request.user.id
    )
    try:
        query_response = get_task_query_handler.handle(query)
        tasks = query_response.content
        if len(tasks) == 0:
            return 404, {"error": "Task not found"}
        return 200, tasks[0]
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}

@task_router.put("/{task_id}", response={200: None, 403: ErrorMessageSchema, 404: ErrorMessageSchema , 500: ErrorMessageSchema}, auth=JWTAuth())
def update_task(request, company_id: UUID, task_id: UUID, task_schema: UpdateTaskSchema):
    command = UpdateTaskCommand(
        task_id=task_id,
        title=task_schema.title,
        description=task_schema.description,
        estimation=task_schema.estimation,
        completed=task_schema.completed,
        user_story_id=task_schema.user_story_id,
        sprint_id=task_schema.sprint_id,
        assigned_user_id=task_schema.assigned_user_id,
        status_column_id=task_schema.status_column_id,
        deleted=task_schema.deleted,
        company_id=company_id,
        requester_user_id=request.user.id
    )
    try:
        update_task_command_handler.handle(command)
        return {"success": True}
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except TaskNotFoundException as exception:
        return 404, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}
