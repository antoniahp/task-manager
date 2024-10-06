from datetime import date
from typing import List, Optional
from uuid import uuid4, UUID

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
from task_manager.domain.sprint.sprint_creator import SprintCreator
from task_manager.domain.sprint_detail.sprint_detail_creator import SprintDetailCreator
from task_manager.domain.sprint_tasks.sprint_tasks_creator import SprintTasksCreator
from task_manager.infrastructure.graphics.graphic_view import task_repository
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.sprints.create_sprint_schema import CreateSprintSchema
from task_manager.infrastructure.sprints.db_sprint_repository import DbSprintRepository
from ninja import Router

from task_manager.infrastructure.sprints.get_sprint_detail_schema import GetSprintDetailSchema
from task_manager.infrastructure.sprints.get_sprints_schema import GetSprintsSchema
from task_manager.infrastructure.sprints.sprint_tasks_column_schema import SprintTasksColumnSchema
from task_manager.infrastructure.sprints.update_sprint_schema import UpdateSprintSchema
from task_manager.infrastructure.status_columns.db_status_column_repository import DbStatusColumnRepository

sprint_router = Router(tags=['sprints'])

sprint_repository = DbSprintRepository()
sprint_creator = SprintCreator()


sprint_detail_creator = SprintDetailCreator()
sprint_tasks_creator = SprintTasksCreator()
status_column_repository = DbStatusColumnRepository()
create_sprint_command_handler = CreateSprintCommandHandler(sprint_repository=sprint_repository, sprint_creator=sprint_creator)
get_sprint_query_handler = GetSprintQueryHandler(sprint_repository=sprint_repository)
update_sprint_command_handler = UpdateSprintCommandHandler(sprint_repository=sprint_repository)
get_sprint_tasks_query_handler = GetSprintTasksQueryHandler(sprint_repository=sprint_repository, status_column_repository=status_column_repository, sprint_tasks_creator=sprint_tasks_creator, task_repository=task_repository)
get_sprint_detail_query_handler = GetSprintDetailQueryHandler(sprint_repository=sprint_repository, task_repository=task_repository, sprint_detail_creator=sprint_detail_creator)
@sprint_router.post("/", response=IdentifierSchema)
def post_sprint(request, create_sprint_schema: CreateSprintSchema):
    id = uuid4()
    command = CreateSprintCommand(
        sprint_id=id,
        name=create_sprint_schema.name,
        objective=create_sprint_schema.objective,
        start_date=create_sprint_schema.start_date,
        end_date=create_sprint_schema.end_date,
        active=create_sprint_schema.active,

    )
    create_sprint_command_handler.handle(command)
    return IdentifierSchema(id=id)


@sprint_router.get("/", response=List[GetSprintsSchema])
def get_sprints(request, sprint_id: Optional[UUID] = None, name: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None, objective: Optional[str] = None, active: Optional[bool] = None):
    query = GetSprintQuery(
        sprint_id=sprint_id,
        name=name,
        objective=objective,
        start_date=start_date,
        end_date=end_date,
        active=active,
    )

    query_response = get_sprint_query_handler.handle(query)
    sprints = query_response.content
    return sprints

@sprint_router.get("/{sprint_id}", response=GetSprintsSchema)
def get_sprints_by_id(request, sprint_id: UUID ):
    query = GetSprintQuery(
        sprint_id=sprint_id,
    )

    query_response = get_sprint_query_handler.handle(query)
    sprint = query_response.content
    return sprint[0]

@sprint_router.get("/{sprint_id}/tasks", response=List[SprintTasksColumnSchema])
def get_sprint_tasks_column(request, sprint_id: UUID):
    query = GetSprintTasksQuery(
        sprint_id=sprint_id
    )
    query_response = get_sprint_tasks_query_handler.handle(query)
    sprint_tasks = query_response.content
    return sprint_tasks.columns



@sprint_router.get("/{sprint_id}/detail", response=GetSprintDetailSchema)
def get_sprint_detail(request, sprint_id: UUID):
    query = GetSprintDetailQuery(
        sprint_id=sprint_id
    )
    query_response = get_sprint_detail_query_handler.handle(query)
    sprint_detail = query_response.content
    return sprint_detail


@sprint_router.put("/{sprint_id}")
def update_sprint(request, sprint_id: UUID, update_schema: UpdateSprintSchema):
    command = UpdateSprintCommand(
        sprint_id=sprint_id,
        name=update_schema.name,
        objective=update_schema.objective,
        start_date=update_schema.start_date,
        end_date=update_schema.end_date,
        active=update_schema.active,
    )
    update_sprint_command_handler.handle(command)
    return {"success": True}

