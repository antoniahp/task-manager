from typing import List

from ninja import Schema

from task_manager.infrastructure.graphics.date_value_graphic_schema import DateValueGraphicSchema
from task_manager.infrastructure.sprints.get_sprints_schema import GetSprintsSchema


class GetSprintDetailSchema(Schema):
    sprint: GetSprintsSchema
    sprint_graphic: List[DateValueGraphicSchema]
