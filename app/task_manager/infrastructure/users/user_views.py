from typing import List, Optional
from uuid import uuid4, UUID

from ninja import Router

from task_manager.application.create_user.create_user_command import CreateUserCommand
from task_manager.application.create_user.create_user_command_handler import CreateUserCommandHandler
from task_manager.application.get_user.get_user_query import GetUserQuery
from task_manager.application.get_user.get_user_query_handler import GetUserQueryHandler
from task_manager.domain.user.user_creator import UserCreator
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.users import db_user_repository
from task_manager.infrastructure.users.create_user_schema import CreateUserSchema
from task_manager.infrastructure.users.db_user_repository import DbUserRepository
from task_manager.infrastructure.users.get_user_schema import GetUserSchema

user_router = Router(tags=["users"])

user_creator = UserCreator()
user_repository = DbUserRepository()
create_user_command_handler = CreateUserCommandHandler(user_creator=user_creator, user_repository=user_repository)
get_user_query_handler = GetUserQueryHandler(user_repository=user_repository)
@user_router.post("/users", response=IdentifierSchema)
def post_user(request, create_user_schema: CreateUserSchema):
    id = uuid4()
    command = CreateUserCommand(
        user_id=id,
        name=create_user_schema.name,
        company=create_user_schema.company,
        username=create_user_schema.username,
        email=create_user_schema.email,
        password=create_user_schema.password
    )
    create_user_command_handler.handle(command)
    return IdentifierSchema(id=id)


@user_router.get("/user/{user_id}", response=GetUserSchema)
def get_user_by_id(request, user_id: UUID ):
    query = GetUserQuery(
        user_id=user_id
    )

    query_response = get_user_query_handler.handle(query)
    user = query_response.content
    return user

@user_router.get("/users/", response=List[GetUserSchema])
def get_users(request, user_id: Optional[UUID] = None, name: Optional[str] = None, company: Optional[str] = None):
    query = GetUserQuery(
        user_id=user_id,
        name=name,
        company=company
    )

    query_response = get_user_query_handler.handle(query)
    users = query_response.content
    return users

