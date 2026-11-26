from datetime import date as date_type

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentUser, get_current_user
from app.bookings.accounting_client import AccountingClient, get_accounting_client
from app.bookings.exceptions import BookingFileError
from app.bookings.schemas import BookingUploadResult
from app.bookings.services.booking_service import process_booking_upload
from app.warehouses.services.warehouse_service import get_warehouse_or_404
from config.database import get_session

router = APIRouter()


@router.post("/{warehouse_id}/bookings/upload", response_model=BookingUploadResult)
async def upload_bookings(
    warehouse_id: int,
    date: date_type = Query(...),
    file: UploadFile = File(...),
    user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    accounting_client: AccountingClient = Depends(get_accounting_client),
) -> dict:
    warehouse = await get_warehouse_or_404(session, warehouse_id, user)
    content = await file.read()
    try:
        return await process_booking_upload(session, accounting_client, warehouse, date, user, content)
    except BookingFileError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
