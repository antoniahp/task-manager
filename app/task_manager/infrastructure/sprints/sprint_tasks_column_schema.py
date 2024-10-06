from typing import List

from ninja import Schema

from task_manager.infrastructure.status_columns.get_status_columns_schema import GetStatusColumnsSchema
from task_manager.infrastructure.task.get_task_schema import GetTaskSchema


class SprintTasksColumnSchema(Schema):
    status_column: GetStatusColumnsSchema
    tasks: List[GetTaskSchema]