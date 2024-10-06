from datetime import timedelta
from typing import List

from task_manager.domain.sprint.sprint import Sprint
from task_manager.domain.sprint_detail.sprint_detail import SprintDetail
from task_manager.domain.sprint_detail.sprint_detail_graphic_item import SprintDetailGraphicItem
from task_manager.domain.task.task import Task


class SprintDetailCreator:
    def create(self, tasks: List[Task], sprint: Sprint) -> SprintDetail:
        mapper_count = {}
        for task in tasks:
            mapper_count_key = task.completed_at.strftime("%Y-%m-%d")
            if mapper_count_key in mapper_count:
                mapper_count[mapper_count_key] = mapper_count[mapper_count_key] + 1
            else:
                mapper_count[mapper_count_key] = 1

        result = []
        current_date = sprint.start_date
        while current_date <= sprint.end_date:
            mapper_count_key = current_date.strftime("%Y-%m-%d")
            result.append(SprintDetailGraphicItem(date=current_date, value=mapper_count.get(mapper_count_key, 0)))
            current_date = current_date + timedelta(days=1)
        return SprintDetail(sprint=sprint, sprint_graphic=result)
