from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QueryResponse:
    content: Optional[any]