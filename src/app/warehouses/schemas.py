from pydantic import BaseModel, ConfigDict
from datetime import date as date_type

class WarehouseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    daily_limit: int


class CalendarDayOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date_type
    occupied: int
    limit: int

