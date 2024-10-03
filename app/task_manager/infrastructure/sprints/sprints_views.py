from datetime import date
from typing import List, Optional
from uuid import uuid4, UUID

from task_manager.application.create_sprint.create_sprint_command import CreateSprintCommand
from task_manager.application.create_sprint.create_sprint_command_handler import CreateSprintCommandHandler
from task_manager.application.get_sprint.get_sprint_query import GetSprintQuery
from task_manager.application.get_sprint.get_sprint_query_handler import GetSprintQueryHandler
from task_manager.application.update_sprint.update_sprint_command import UpdateSprintCommand
from task_manager.application.update_sprint.update_sprint_command_handler import UpdateSprintCommandHandler
from task_manager.domain.sprint.sprint_creator import SprintCreator
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.sprints.create_sprint_schema import CreateSprintSchema
from task_manager.infrastructure.sprints.db_sprint_repository import DbSprintRepository
from ninja import Router

from task_manager.infrastructure.sprints.get_sprints_schema import GetSprintsSchema
from task_manager.infrastructure.sprints.update_sprint_schema import UpdateSprintSchema

sprint_router = Router(tags=['sprints'])

sprint_repository = DbSprintRepository()
sprint_creator = SprintCreator()
create_sprint_command_handler = CreateSprintCommandHandler(sprint_repository=sprint_repository, sprint_creator=sprint_creator)
get_sprint_query_handler = GetSprintQueryHandler(sprint_repository=sprint_repository)
update_sprint_command_handler = UpdateSprintCommandHandler(sprint_repository=sprint_repository)

@sprint_router.post("/sprints", response=IdentifierSchema)
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


@sprint_router.get("/sprints", response=List[GetSprintsSchema])
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




@sprint_router.put("/sprint/{sprint_id}")
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