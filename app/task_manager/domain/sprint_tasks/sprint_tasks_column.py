from dataclasses import dataclass
from typing import List

from task_manager.domain.status_column.status_column import StatusColumn
from task_manager.domain.task.task import Task


@dataclass(frozen=True)
class SprintTasksColumn:
    status_column : StatusColumn
    tasks: List[Task]