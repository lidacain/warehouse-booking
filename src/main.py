from fastapi import FastAPI
from app.warehouses.api import router as warehouses_router
from app.bookings.api import router as bookings_router

app = FastAPI(title="Warehouse Booking API")

app.include_router(warehouses_router)

app.include_router(bookings_router)
