from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import CurrentUser
from app.warehouses.models.warehouse import Warehouse
from fastapi import HTTPException


async def list_warehouses(session: AsyncSession, user: CurrentUser) -> list[Warehouse]:
    stmt = select(Warehouse)
    if user.org_type != "company":
        stmt = stmt.where(Warehouse.organization_id == user.org_id)
    result = await session.scalars(stmt)
    return list(result)

async def get_warehouse_or_404(
    session: AsyncSession, warehouse_id: int, user: CurrentUser
) -> Warehouse:
    warehouse = await session.get(Warehouse, warehouse_id)
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Склад не найден")
    if user.org_type != "company" and warehouse.organization_id != user.org_id:
        raise HTTPException(status_code=404, detail="Склад не найден")
    return warehouse


