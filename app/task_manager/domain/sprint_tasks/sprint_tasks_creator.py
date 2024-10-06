from typing import List

from task_manager.domain.sprint_tasks.sprint_tasks import SprintTasks
from task_manager.domain.sprint_tasks.sprint_tasks_column import SprintTasksColumn
from task_manager.domain.status_column.status_column import StatusColumn
from task_manager.domain.task.task import Task


class SprintTasksCreator:
    def create(self, tasks: List[Task], columns: List[StatusColumn]) -> SprintTasks:
        column_id_tasks_mapper = {}
        for task in tasks:
            key = task.status_column_id
            if key in column_id_tasks_mapper:
                column_id_tasks_mapper[key].append(task)
            else:
                column_id_tasks_mapper[key] = [task]

        column_id_columns_mapper = {}
        for column in columns:
            key = column.id
            column_id_columns_mapper[key] = column

        sprint_tasks_columns = []
        for column_id, column in column_id_columns_mapper.items():
            tasks = column_id_tasks_mapper.get(column_id, [])
            sprint_tasks_columns.append(SprintTasksColumn(status_column=column, tasks=tasks))

        return SprintTasks(columns=sprint_tasks_columns)