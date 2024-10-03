from datetime import date
from ninja import Schema

class CreateSprintSchema(Schema):
    name: str
    objective: str
    start_date: date
    end_date: date
    active: bool
