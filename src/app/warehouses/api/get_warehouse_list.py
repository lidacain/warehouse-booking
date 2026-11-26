from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import CurrentUser, get_current_user
from app.warehouses.models.warehouse import Warehouse
from app.warehouses.schemas import WarehouseOut
from app.warehouses.services.warehouse_service import list_warehouses
from config.database import get_session

router = APIRouter()


@router.get("", response_model=list[WarehouseOut])
async def get_warehouse_list(
        session: AsyncSession = Depends(get_session),
        user: CurrentUser = Depends(get_current_user)
) -> list[Warehouse]:
    return await list_warehouses(session, user)