from datetime import datetime

from ninja import Schema


class DateValueGraphicSchema(Schema):
    date: datetime
    value: int
