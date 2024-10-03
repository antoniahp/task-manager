from datetime import date

from ninja import Schema


class CreateProjectSchema(Schema):
    name: str
    start_date: date
    end_date: date