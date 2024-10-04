from datetime import date
from typing import Optional
from uuid import UUID

from ninja import Schema


class CreateStatusColumnSchema(Schema):
    name: str
    company_id: Optional[UUID]
