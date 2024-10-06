from typing import List, Optional
from uuid import UUID, uuid4

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from task_manager.application.create_status_column.create_status_column_command import CreateStatusColumnCommand
from task_manager.application.create_status_column.create_status_column_command_handler import CreateStatusColumnCommandHandler
from task_manager.application.get_status_column.get_status_column_query import GetStatusColumnQuery
from task_manager.application.get_status_column.get_status_column_query_handler import GetStatusColumnQueryHandler
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.status_column.status_column_creator import StatusColumnCreator
from task_manager.infrastructure.error_message_schema import ErrorMessageSchema
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.status_columns.create_status_column_schema import CreateStatusColumnSchema
from task_manager.infrastructure.status_columns.db_status_column_repository import DbStatusColumnRepository
from task_manager.infrastructure.status_columns.get_status_columns_schema import GetStatusColumnsSchema
from task_manager.infrastructure.users.db_user_repository import DbUserRepository

status_columns_router = Router(tags=["status columns"])

status_column_repository = DbStatusColumnRepository()
user_repository = DbUserRepository()
status_column_creator = StatusColumnCreator()
get_status_column_query_handler = GetStatusColumnQueryHandler(
    status_column_repository=status_column_repository,
    user_repository=user_repository
)
create_status_column_command_handler = CreateStatusColumnCommandHandler(
    status_column_repository=status_column_repository,
    status_column_creator=status_column_creator,
    user_repository=user_repository
)


@status_columns_router.post("/", response={200: IdentifierSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def create_status_column(request, create_status_columns_schema: CreateStatusColumnSchema):
    id = uuid4()
    command = CreateStatusColumnCommand(
        status_column_id=id,
        name=create_status_columns_schema.name,
        company_id=create_status_columns_schema.company_id,
        order=create_status_columns_schema.order,
        requester_user_id=request.user.id,
    )
    try:
        create_status_column_command_handler.handle(command)
        return IdentifierSchema(id=id)
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@status_columns_router.get("/", response={200: List[GetStatusColumnsSchema], 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_status_columns(request, company_id: UUID, name: Optional[str] = None):
    query = GetStatusColumnQuery(
        name=name,
        company_id=company_id,
        requester_user_id=request.user.id,
    )
    try:
        query_response = get_status_column_query_handler.handle(query)
        status_columns = query_response.content
        return status_columns
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@status_columns_router.get("/{status_column_id}", response={200: GetStatusColumnsSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_status_column_by_id(request, company_id: UUID, status_column_id: UUID):
    query = GetStatusColumnQuery(
        status_column_id=status_column_id,
        requester_user_id=request.user.id,
        company_id=company_id
    )
    try:
        query_response = get_status_column_query_handler.handle(query)
        status_column = query_response.content
        return status_column[0]
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}
