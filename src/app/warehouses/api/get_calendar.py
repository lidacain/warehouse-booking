from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentUser, get_current_user
from app.warehouses.schemas import CalendarDayOut
from app.warehouses.services.calendar_service import get_month_calendar
from app.warehouses.services.warehouse_service import get_warehouse_or_404
from config.database import get_session

router = APIRouter()


@router.get("/{warehouse_id}/calendar", response_model=list[CalendarDayOut])
async def get_calendar(
        warehouse_id: int,
        year: int = Query(..., ge=2000, le=2100),
        month: int = Query(..., ge=1, le=12),
        session: AsyncSession = Depends(get_session),
        user: CurrentUser = Depends(get_current_user)
) -> list[dict]:
    warehouse = await get_warehouse_or_404(session, warehouse_id, user)
    return await get_month_calendar(session, warehouse, year, month)