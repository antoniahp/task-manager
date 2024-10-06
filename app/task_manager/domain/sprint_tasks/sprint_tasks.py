from dataclasses import dataclass
from typing import List

from task_manager.domain.sprint_tasks.sprint_tasks_column import SprintTasksColumn


@dataclass(frozen=True)
class SprintTasks:
    columns: List[SprintTasksColumn]