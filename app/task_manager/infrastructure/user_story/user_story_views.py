from typing import List, Optional
from uuid import uuid4, UUID

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from task_manager.application.create_user_story.create_user_story_command import CreateUserStoryCommand
from task_manager.application.create_user_story.create_user_story_command_handler import CreateUserStoryCommandHandler
from task_manager.application.get_user_story.get_user_story_query import GetUserStoryQuery
from task_manager.application.get_user_story.get_user_story_query_handler import GetUserStoryQueryHandler
from task_manager.application.update_user_story.update_user_story_command import UpdateUserStoryCommand
from task_manager.application.update_user_story.update_user_story_command_handler import UpdateUserStoryCommandHandler
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_story_not_found_exception import UserStoryNotFoundException
from task_manager.domain.user_story.user_story_creator import UserStoryCreator
from task_manager.infrastructure.error_message_schema import ErrorMessageSchema
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.user_story.create_user_story_schema import CreateUserStorySchema
from task_manager.infrastructure.user_story.db_user_story_repository import DbUserStoryRepository
from task_manager.infrastructure.user_story.get_user_story_schema import GetUserStorySchema
from task_manager.infrastructure.user_story.update_user_story_schema import UpdateUserStorySchema
from task_manager.infrastructure.users.db_user_repository import DbUserRepository

user_story_router = Router(tags=["user_story"])

user_repository = DbUserRepository()
user_story_repository=DbUserStoryRepository()
user_story_creator=UserStoryCreator()
create_user_story_command_handler = CreateUserStoryCommandHandler(user_story_creator=user_story_creator, user_story_repository=user_story_repository, user_repository=user_repository)
get_user_story_query_handler = GetUserStoryQueryHandler(user_story_repository=user_story_repository, user_repository=user_repository)
update_user_story_command_handler = UpdateUserStoryCommandHandler(user_story_repository=user_story_repository,user_repository=user_repository)
@user_story_router.post("/", response={200: IdentifierSchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def create_user_story(request, company_id: UUID, create_user_story_schema: CreateUserStorySchema):
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
        completed_at=create_user_story_schema.completed_at,
        company_id=company_id,
        requester_user_id=request.user.id,
    )

    try:
        create_user_story_command_handler.handle(command)
        return IdentifierSchema(id=id)
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@user_story_router.get("/", response={200: List[GetUserStorySchema], 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_user_stories(request, company_id:UUID, title: Optional[str] = None, description: Optional[str] = None, estimation: Optional[int] = None,
             completed: Optional[bool] = None, project_id: Optional[UUID] = None, assigned_user_id: Optional[UUID] = None, status_column_id: Optional[UUID] = None):
    query = GetUserStoryQuery(
        title=title,
        description=description,
        estimation=estimation,
        completed=completed,
        project_id=project_id,
        assigned_user_id=assigned_user_id,
        status_column_id=status_column_id,
        company_id=company_id,
        requester_user_id=request.user.id,

    )
    try:
        query_response = get_user_story_query_handler.handle(query)
        user_stories = query_response.content
        return user_stories
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}

@user_story_router.get("/{user_story_id}", response={200: GetUserStorySchema, 403: ErrorMessageSchema, 500: ErrorMessageSchema}, auth=JWTAuth())
def get_user_story_by_id(request, company_id:UUID, user_story_id: UUID):
    query = GetUserStoryQuery(
        user_story_id=user_story_id,
        company_id=company_id,
        requester_user_id=request.user.id
    )
    try:
        query_response = get_user_story_query_handler.handle(query)
        user_story = query_response.content
        return user_story[0]
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}


@user_story_router.put("/{user_story_id}", response={200: None, 403: ErrorMessageSchema, 404: ErrorMessageSchema , 500: ErrorMessageSchema}, auth=JWTAuth())
def update_user_story(request, company_id: UUID, user_story_id: UUID, user_story_schema: UpdateUserStorySchema):
    command = UpdateUserStoryCommand(
        user_story_id=user_story_id,
        title=user_story_schema.title,
        description=user_story_schema.description,
        estimation=user_story_schema.estimation,
        completed=user_story_schema.completed,
        project_id=user_story_schema.project_id,
        assigned_user_id=user_story_schema.assigned_user_id,
        status_column_id=user_story_schema.status_column_id,
        company_id=company_id,
        requester_user_id=request.user.id

    )
    try:
        update_user_story_command_handler.handle(command)
        return {"success": True}
    except UserDoesNotBelongToCompanyException as exception:
        return 403, {"error": str(exception)}
    except UserStoryNotFoundException as exception:
        return 404, {"error": str(exception)}
    except Exception as exception:
        return 500, {"error": str(exception)}
