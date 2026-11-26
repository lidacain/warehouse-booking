from datetime import date as date_type

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentUser, get_current_user
from app.warehouses.schemas import CalendarDayOut
from app.warehouses.services.calendar_service import get_day_availability
from app.warehouses.services.warehouse_service import get_warehouse_or_404
from config.database import get_session

router = APIRouter()


@router.get("/{warehouse_id}/availability", response_model=CalendarDayOut)
async def get_availability(
    warehouse_id: int,
    date: date_type = Query(...),
    user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    warehouse = await get_warehouse_or_404(session, warehouse_id, user)
    return await get_day_availability(session, warehouse, date)
