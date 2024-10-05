from typing import List, Optional
from uuid import UUID, uuid4

from ninja import Router

from task_manager.application.create_status_column.create_status_column_command import CreateStatusColumnCommand
from task_manager.application.create_status_column.create_status_column_command_handler import CreateStatusColumnCommandHandler
from task_manager.application.get_status_column.get_status_column_query import GetStatusColumnQuery
from task_manager.application.get_status_column.get_status_column_query_handler import GetStatusColumnQueryHandler
from task_manager.domain.status_column.status_column_creator import StatusColumnCreator
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.status_columns.create_status_column_schema import CreateStatusColumnSchema
from task_manager.infrastructure.status_columns.db_status_column_repository import DbStatusColumnRepository
from task_manager.infrastructure.status_columns.get_status_columns_schema import GetStatusColumnsSchema

status_columns_router = Router(tags=["status columns"])

status_column_repository = DbStatusColumnRepository()
status_column_creator = StatusColumnCreator()
get_status_column_query_handler = GetStatusColumnQueryHandler(status_column_repository=status_column_repository)
create_status_column_command_handler = CreateStatusColumnCommandHandler(status_column_repository=status_column_repository, status_column_creator=status_column_creator)

@status_columns_router.get("/status_columns", response=List[GetStatusColumnsSchema])
def get_status_columns(request, name: Optional[str] = None, company_id: Optional[UUID] = None, order: Optional[int] = None,):
    query = GetStatusColumnQuery(
        name=name,
        company_id=company_id,
        order=order
    )

    query_response = get_status_column_query_handler.handle(query)
    status_columns = query_response.content
    return status_columns



@status_columns_router.post("/status-columns", response=IdentifierSchema)
def post_status_columns(request, create_status_columns_schema: CreateStatusColumnSchema):
    id = uuid4()
    command = CreateStatusColumnCommand(
        status_column_id=id,
        name=create_status_columns_schema.name,
        company_id=create_status_columns_schema.company_id,
        order=create_status_columns_schema.order
    )
    create_status_column_command_handler.handle(command)
    return IdentifierSchema(id=id)


@status_columns_router.get("/status-columns/{status_column_id}", response=GetStatusColumnsSchema)
def get_status_columns_by_id(request, status_column_id: UUID):
    query = GetStatusColumnQuery(
        status_column_id=status_column_id,
    )

    query_response = get_status_column_query_handler.handle(query)
    status_column = query_response.content
    return status_column[0]
