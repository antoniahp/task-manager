from typing import List, Optional
from uuid import uuid4, UUID

from task_manager.application.create_task.create_task_command import CreateTaskCommand
from task_manager.application.create_task.create_task_command_handler import CreateTaskCommandHandler
from task_manager.application.get_task.get_task_query import GetTaskQuery
from task_manager.application.get_task.get_task_query_handler import GetTaskQueryHandler
from task_manager.domain.task.task_creator import TaskCreator
from task_manager.infrastructure.task.get_task_schema import GetTaskSchema
from task_manager.infrastructure.task.create_task_schema import CreateTaskSchema
from task_manager.infrastructure.task.db_task_repository import DbTaskRepository
from ninja import Router

from task_manager.infrastructure.identifier_schema import IdentifierSchema

task_router = Router(tags=["tasks"])

task_repository = DbTaskRepository()
task_creator = TaskCreator()
create_task_command_handler = CreateTaskCommandHandler(task_repository=task_repository, task_creator=task_creator)
get_task_query_handler = GetTaskQueryHandler(task_repository=task_repository)



@task_router.post("/task", response=IdentifierSchema)
def post_task(request, create_task_schema: CreateTaskSchema):
    id = uuid4()
    command = CreateTaskCommand(
        task_id=id,
        title=create_task_schema.title,
        description=create_task_schema.description,
        estimation=create_task_schema.estimation,
        completed=create_task_schema.completed,
        category=create_task_schema.category,
        parent_task=create_task_schema.parent_task,
        sprint=create_task_schema.sprint,
        project=create_task_schema.project,
        user=create_task_schema.user
    )
    create_task_command_handler.handle(command)
    return IdentifierSchema(id=id)



@task_router.get("/task", response=List[GetTaskSchema])
def get_task(request, task_id: Optional[UUID] = None, title: Optional[str] = None,
             description: Optional[str] = None, estimation: Optional[int] = None,
             completed: Optional[bool] = None, category: Optional[str] = None,
             parent_task: Optional[UUID] = None, sprint: Optional[UUID] = None,
             project: Optional[UUID] = None, user: Optional[UUID] = None):
    query = GetTaskQuery(
        task_id=task_id,
        title=title,
        description=description,
        estimation=estimation,
        completed=completed,
        category=category,
        parent_task=parent_task,
        sprint=sprint,
        project=project,
        user=user,
    )

    query_response = get_task_query_handler.handle(query)
    tasks = query_response.content
    # Serialize the response correctly
    serialized_tasks = [
        {
            "task_id": str(task.id),
            "title": task.title,
            "description": task.description,
            "estimation": task.estimation,
            "completed": task.completed,
            "category": task.category,
            "parent_task": str(task.parent_task) if task.parent_task else None,
            "sprint": str(task.sprint.id) if task.sprint else None,
            "project": str(task.project.id) if task.project else None,
            "user": str(task.user.id) if task.user else None,
        }
        for task in tasks
    ]

    return serialized_tasks
