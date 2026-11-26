from datetime import date as date_type
from typing import Literal

from pydantic import BaseModel


class BookingRowResult(BaseModel):
    row: int
    vin: str
    status: Literal["booked", "rejected"]
    reason: str | None = None


class BookingUploadResult(BaseModel):
    warehouse_id: int
    date: date_type
    total_rows: int
    booked_count: int
    rejected_count: int
    results: list[BookingRowResult]
