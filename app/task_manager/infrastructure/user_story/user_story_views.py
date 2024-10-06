from typing import List, Optional
from uuid import uuid4, UUID

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from task_manager.application.get_user_story.get_user_story_query import GetUserStoryQuery
from task_manager.application.get_user_story.get_user_story_query_handler import GetUserStoryQueryHandler
from task_manager.application.update_user_story.update_user_story_command import UpdateUserStoryCommand
from task_manager.application.update_user_story.update_user_story_command_handler import UpdateUserStoryCommandHandler
from task_manager.create_user_story.create_user_story_command import CreateUserStoryCommand
from task_manager.create_user_story.create_user_story_command_handler import CreateUserStoryCommandHandler
from task_manager.domain.user_story.user_story_creator import UserStoryCreator
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.user_story.create_user_story_schema import CreateUserStorySchema
from task_manager.infrastructure.user_story.db_user_story_repository import DbUserStoryRepository
from task_manager.infrastructure.user_story.get_user_story_schema import GetUserStorySchema
from task_manager.infrastructure.user_story.update_user_story_schema import UpdateUserStorySchema

user_story_router = Router(tags=["user_story"])

user_story_repository=DbUserStoryRepository()
user_story_creator=UserStoryCreator()
create_user_story_command_handler = CreateUserStoryCommandHandler(user_story_creator=user_story_creator, user_story_repository=user_story_repository)
get_user_story_query_handler = GetUserStoryQueryHandler(user_story_repository=user_story_repository)
update_user_story_command_handler = UpdateUserStoryCommandHandler(user_story_repository=user_story_repository)
@user_story_router.post("/", response=IdentifierSchema)
def create_user_story(request, create_user_story_schema: CreateUserStorySchema):
    id = uuid4()
    command = CreateUserStoryCommand(
        user_story_id=id,
        title=create_user_story_schema.title,
        description=create_user_story_schema.description,
        estimation=create_user_story_schema.estimation,
        completed=create_user_story_schema.completed,
        project_id=create_user_story_schema.project_id,
        assigned_user_id=create_user_story_schema.assigned_user_id,
        status_column_id=create_user_story_schema.status_column_id,
        completed_at=create_user_story_schema.completed_at
    )


    create_user_story_command_handler.handle(command)
    return IdentifierSchema(id=id)


@user_story_router.get("/", response=List[GetUserStorySchema])
def get_user_stories(request, title: Optional[str] = None, description: Optional[str] = None, estimation: Optional[int] = None,
             completed: Optional[bool] = None, project_id: Optional[UUID] = None, assigned_user_id: Optional[UUID] = None, status_column_id: Optional[UUID] = None):
    query = GetUserStoryQuery(
        title=title,
        description=description,
        estimation=estimation,
        completed=completed,
        project_id=project_id,
        assigned_user_id=assigned_user_id,
        status_column_id=status_column_id
    )
    query_response = get_user_story_query_handler.handle(query)
    user_stories = query_response.content
    return user_stories


@user_story_router.get("/{user_story_id}", response=GetUserStorySchema)
def get_user_story_by_id(request, user_story_id: UUID):
    query = GetUserStoryQuery(
        user_story_id=user_story_id,
    )

    query_response = get_user_story_query_handler.handle(query)
    user_story = query_response.content
    return user_story[0]


@user_story_router.put("/{user_story_id}")
def update_user_story(request, user_story_id: UUID, user_story_schema: UpdateUserStorySchema):
    command = UpdateUserStoryCommand(
        user_story_id=user_story_id,
        title=user_story_schema.title,
        description=user_story_schema.description,
        estimation=user_story_schema.estimation,
        completed=user_story_schema.completed,
        project_id=user_story_schema.project_id,
        assigned_user_id=user_story_schema.assigned_user_id,
        status_column_id=user_story_schema.status_column_id
    )
    update_user_story_command_handler.handle(command)
    return {"success": True}