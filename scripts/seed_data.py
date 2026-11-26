import asyncio
import os
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.bookings.models.vehicle_booking import VehicleBooking
from app.organizations.models.organization import Organization
from app.warehouses.models.warehouse import Warehouse
from config.database import SessionLocal


async def seed() -> None:
    async with SessionLocal() as session:
        astana_motors = Organization(name="Астана Моторс", type=Organization.Type.COMPANY)
        distributor_a = Organization(name="Дистрибьютор А", type=Organization.Type.DISTRIBUTOR)
        distributor_b = Organization(name="Дистрибьютор Б", type=Organization.Type.DISTRIBUTOR)
        session.add_all([astana_motors, distributor_a, distributor_b])
        await session.flush()

        warehouse_a = Warehouse(name="Склад Алматы", organization_id=distributor_a.id, daily_limit=5)
        warehouse_b = Warehouse(name="Склад Астана", organization_id=distributor_b.id, daily_limit=3)
        session.add_all([warehouse_a, warehouse_b])
        await session.flush()

        today = date.today()
        session.add_all([
            VehicleBooking(
                vin="LVVDB21B4RD012401",
                warehouse_id=warehouse_a.id,
                booking_date=today,
                organization_id=distributor_a.id,
            ),
            VehicleBooking(
                vin="XWEPC81BDR0004421",
                warehouse_id=warehouse_a.id,
                booking_date=today,
                organization_id=distributor_a.id,
            ),
            VehicleBooking(
                vin="JN1TENT32Z0123456",
                warehouse_id=warehouse_b.id,
                booking_date=today + timedelta(days=1),
                organization_id=distributor_b.id,
            ),
        ])
        await session.commit()
        print("Готово: 3 организации, 2 склада, 3 активные записи.")


if __name__ == "__main__":
    asyncio.run(seed())