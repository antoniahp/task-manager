from dataclasses import dataclass
from typing import List

from task_manager.domain.sprint.sprint import Sprint
from task_manager.domain.sprint_detail.sprint_detail_graphic_item import SprintDetailGraphicItem


@dataclass(frozen=True)
class SprintDetail:
    sprint: Sprint
    sprint_graphic: List[SprintDetailGraphicItem]