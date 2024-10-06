from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SprintDetailGraphicItem:
    date: datetime
    value: int