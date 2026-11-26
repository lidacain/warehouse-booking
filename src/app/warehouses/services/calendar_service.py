import calendar as calendar_module
from datetime import date
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.bookings.models.vehicle_booking import VehicleBooking
from app.warehouses.models.warehouse import Warehouse


async def get_month_calendar(
        session: AsyncSession,
        warehouse: Warehouse,
        year: int,
        month: int
) -> list[dict]:
    _, days_in_month = calendar_module.monthrange(year, month)

    stmt = (
        select(VehicleBooking.booking_date, func.count())
        .where(
            VehicleBooking.warehouse_id == warehouse.id,
            VehicleBooking.status == VehicleBooking.Status.ACTIVE,
            VehicleBooking.booking_date >= date(year, month, 1),
            VehicleBooking.booking_date <= date(year, month, days_in_month),
        )
        .group_by(VehicleBooking.booking_date)
    )
    result = await session.execute(stmt)
    occupied_by_date = dict(result.all())

    return [
        {
            "date": date(year, month, day),
            "occupied": occupied_by_date.get(date(year, month, day), 0),
            "limit": warehouse.daily_limit,
        }
        for day in range(1, days_in_month + 1)
    ]


async def get_day_availability(
    session: AsyncSession, warehouse: Warehouse, target_date: date
) -> dict:
    stmt = (
        select(func.count())
        .select_from(VehicleBooking)
        .where(
            VehicleBooking.warehouse_id == warehouse.id,
            VehicleBooking.status == VehicleBooking.Status.ACTIVE,
            VehicleBooking.booking_date == target_date,
        )
    )
    occupied = await session.scalar(stmt)
    return {"date": target_date, "occupied": occupied, "limit": warehouse.daily_limit}


