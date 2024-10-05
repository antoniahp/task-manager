from datetime import datetime, timedelta
from typing import List

from task_manager.domain.task.task import Task
from task_manager.infrastructure.graphics.date_value_graphic_schema import DateValueGraphicSchema


class TasksToDateValueGraphSchemaAdapter:
    def adapt(self, tasks: List[Task], start_date: datetime, end_date: datetime) -> List[DateValueGraphicSchema]:
        mapper_count = {}
        for task in tasks:
            mapper_count_key = task.completed_at.strftime("%Y-%m-%d")
            if mapper_count_key in mapper_count:
                mapper_count[mapper_count_key] = mapper_count[mapper_count_key] + 1
            else:
                mapper_count[mapper_count_key] = 1

        result = []
        current_date = start_date
        while current_date <= end_date:
            mapper_count_key = current_date.strftime("%Y-%m-%d")
            result.append(DateValueGraphicSchema(date=current_date, value=mapper_count.get(mapper_count_key, 0)))
            current_date = current_date + timedelta(days=1)
        return result


