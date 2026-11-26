from datetime import UTC, date as date_type, datetime
from io import BytesIO

import openpyxl
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentUser
from app.bookings.accounting_client import AccountingClient
from app.bookings.exceptions import PastDateError, TooManyRowsError, VinColumnNotFoundError
from app.bookings.models.vehicle_booking import VehicleBooking
from app.warehouses.models.warehouse import Warehouse

MAX_ROWS = 200
VIN_LENGTH = 17


def _parse_vin_rows(content: bytes) -> list[tuple[int, str]]:
    workbook = openpyxl.load_workbook(BytesIO(content), read_only=True, data_only=True)
    sheet = workbook.active

    header_row = next(sheet.iter_rows(min_row=1, max_row=1))
    header = [str(cell.value).strip() if cell.value is not None else "" for cell in header_row]
    if "VIN" not in header:
        raise VinColumnNotFoundError
    vin_col_index = header.index("VIN")

    rows: list[tuple[int, str]] = []
    for row_number, row in enumerate(sheet.iter_rows(min_row=2), start=2):
        if vin_col_index >= len(row):
            continue
        value = row[vin_col_index].value
        if value is None or str(value).strip() == "":
            continue
        rows.append((row_number, str(value).strip()))

    if len(rows) > MAX_ROWS:
        raise TooManyRowsError(len(rows))

    return rows


async def process_booking_upload(
    session: AsyncSession,
    accounting_client: AccountingClient,
    warehouse: Warehouse,
    target_date: date_type,
    user: CurrentUser,
    file_content: bytes,
) -> dict:
    if target_date < datetime.now(UTC).date():
        raise PastDateError

    rows = _parse_vin_rows(file_content)

    results: dict[int, dict] = {}
    seen_vins: dict[str, int] = {}
    valid_rows: list[tuple[int, str]] = []

    for row_number, vin in rows:
        if len(vin) != VIN_LENGTH:
            results[row_number] = {
                "row": row_number, "vin": vin, "status": "rejected",
                "reason": f"Неверный VIN — {len(vin)} символов",
            }
            continue
        if vin in seen_vins:
            results[row_number] = {
                "row": row_number, "vin": vin, "status": "rejected",
                "reason": f"Повторяется в файле (строка {seen_vins[vin]})",
            }
            continue
        seen_vins[vin] = row_number
        valid_rows.append((row_number, vin))

    unique_vins = list({vin for _, vin in valid_rows})
    found = await accounting_client.lookup_vins(unique_vins) if unique_vins else set()

    already_active: set[str] = set()
    if unique_vins:
        stmt = select(VehicleBooking.vin).where(
            VehicleBooking.vin.in_(unique_vins),
            VehicleBooking.status == VehicleBooking.Status.ACTIVE,
        )
        already_active = set((await session.scalars(stmt)).all())

    await session.execute(
        text("SELECT pg_advisory_xact_lock(hashtext(:key))"),
        {"key": f"{warehouse.id}:{target_date}"},
    )
    occupied_stmt = (
        select(func.count())
        .select_from(VehicleBooking)
        .where(
            VehicleBooking.warehouse_id == warehouse.id,
            VehicleBooking.status == VehicleBooking.Status.ACTIVE,
            VehicleBooking.booking_date == target_date,
        )
    )
    occupied = await session.scalar(occupied_stmt)
    free_slots = warehouse.daily_limit - occupied

    to_insert: list[VehicleBooking] = []
    for row_number, vin in valid_rows:
        if vin not in found:
            results[row_number] = {"row": row_number, "vin": vin, "status": "rejected", "reason": "Нет в учёте"}
        elif vin in already_active:
            results[row_number] = {"row": row_number, "vin": vin, "status": "rejected", "reason": "Уже есть активная запись"}
        elif free_slots > 0:
            to_insert.append(
                VehicleBooking(
                    vin=vin,
                    warehouse_id=warehouse.id,
                    booking_date=target_date,
                    organization_id=user.org_id,
                )
            )
            results[row_number] = {"row": row_number, "vin": vin, "status": "booked", "reason": None}
            free_slots -= 1
        else:
            results[row_number] = {"row": row_number, "vin": vin, "status": "rejected", "reason": "Не хватило мест"}

    session.add_all(to_insert)
    await session.commit()

    ordered_results = [results[row_number] for row_number, _ in rows]
    booked_count = sum(1 for r in ordered_results if r["status"] == "booked")

    return {
        "warehouse_id": warehouse.id,
        "date": target_date,
        "total_rows": len(rows),
        "booked_count": booked_count,
        "rejected_count": len(rows) - booked_count,
        "results": ordered_results,
    }
