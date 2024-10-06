from datetime import datetime
from typing import List

from ninja import Router

from task_manager.application.get_task.get_task_query import GetTaskQuery
from task_manager.application.get_task.get_task_query_handler import GetTaskQueryHandler
from task_manager.infrastructure.graphics.date_value_graphic_schema import DateValueGraphicSchema
from task_manager.infrastructure.graphics.task_to_date_value_graph_schema_adaptor import TasksToDateValueGraphSchemaAdapter
from task_manager.infrastructure.task.db_task_repository import DbTaskRepository

graphics_router = Router(tags=["graphics"])

task_repository = DbTaskRepository()
get_task_query_handler = GetTaskQueryHandler(task_repository=task_repository)
task_to_date_value_graph_schema_adaptor = TasksToDateValueGraphSchemaAdapter()


@graphics_router.get("/graphics", response=List[DateValueGraphicSchema])
def get_graphic(request, start_date: datetime, end_date: datetime):
    query = GetTaskQuery(
        completed_at__lte=end_date,
        completed_at__gte=start_date,
    )

    query_response = get_task_query_handler.handle(query)
    tasks = query_response.content
    return task_to_date_value_graph_schema_adaptor.adapt(tasks=tasks, start_date=start_date, end_date=end_date)