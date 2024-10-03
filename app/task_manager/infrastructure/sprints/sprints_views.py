from uuid import uuid4

from django.http import JsonResponse

from task_manager.application.create_task.create_task_command import CreateTaskCommand
from task_manager.application.create_task.create_task_command_handler import CreateTaskCommandHandler
from task_manager.domain.task.task_creator import TaskCreator
from task_manager.infrastructure.task.create_task_schema import CreateTaskSchema
from task_manager.infrastructure.task.db_task_repository import DbTaskRepository
from ninja import Router

sprint_router = Router(tags=['sprints'])

task_repository = DbTaskRepository()
task_creator = TaskCreator()
create_task_command_handler = CreateTaskCommandHandler(task_repository=task_repository, task_creator=task_creator)

@sprint_router.post("/sprints")
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
    return JsonResponse({'id': str(id)}, status=201)

