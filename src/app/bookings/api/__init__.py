from fastapi import APIRouter

from app.bookings.api import upload_bookings

router = APIRouter(tags=["bookings"])
router.include_router(upload_bookings.router, prefix="/warehouses")
