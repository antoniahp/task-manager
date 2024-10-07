from typing import List, Optional
from uuid import uuid4, UUID

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from task_manager.application.create_user.create_user_command import CreateUserCommand
from task_manager.application.create_user.create_user_command_handler import CreateUserCommandHandler
from task_manager.application.get_user.get_user_query import GetUserQuery
from task_manager.application.get_user.get_user_query_handler import GetUserQueryHandler
from task_manager.domain.user.user_creator import UserCreator
from task_manager.infrastructure.companies.db_company_repository import DbCompanyRepository
from task_manager.infrastructure.identifier_schema import IdentifierSchema
from task_manager.infrastructure.users.create_user_schema import CreateUserSchema
from task_manager.infrastructure.users.db_user_repository import DbUserRepository
from task_manager.infrastructure.users.get_user_schema import GetUserSchema

user_router = Router(tags=["users"])

user_creator = UserCreator()
user_repository = DbUserRepository()
company_repository = DbCompanyRepository()
create_user_command_handler = CreateUserCommandHandler(user_creator=user_creator, user_repository=user_repository, company_repository=company_repository)
get_user_query_handler = GetUserQueryHandler(user_repository=user_repository)


@user_router.post("/", response=IdentifierSchema)
def create_user(request, create_user_schema: CreateUserSchema):
    id = uuid4()
    command = CreateUserCommand(
        user_id=id,
        name=create_user_schema.name,
        company_id=create_user_schema.company_id,
        username=create_user_schema.username,
        email=create_user_schema.email,
        password=create_user_schema.password
    )
    create_user_command_handler.handle(command)
    return IdentifierSchema(id=id)


@user_router.get("/logged-user", response=GetUserSchema,  auth=JWTAuth())
def get_logged_user(request):
    query = GetUserQuery(
        user_id=request.user.id
    )

    query_response = get_user_query_handler.handle(query)
    user = query_response.content
    return user

