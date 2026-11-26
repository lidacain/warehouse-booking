from fastapi import APIRouter
from app.warehouses.api import get_warehouse_list, get_calendar, get_availability


router = APIRouter(tags=["warehouses"])
router.include_router(get_warehouse_list.router, prefix="/warehouses")
router.include_router(get_calendar.router, prefix="/warehouses")
router.include_router(get_availability.router, prefix="/warehouses")
