from datetime import date

from ninja import Schema


class UpdateSprintSchema(Schema):
    name: str
    objective: str
    start_date: date
    end_date: date
    active: bool
