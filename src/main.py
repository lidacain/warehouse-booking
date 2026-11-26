from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_session
from app.auth.dependencies import CurrentUser, get_current_user
from app.organizations.models.organization import Organization  # noqa: F401


app = FastAPI(title="lidacain")

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/health/db")
async def health_db(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/health/me")
async def health_me(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    return user


from app.warehouses.api import router as warehouses_router
app.include_router(warehouses_router)


from app.bookings.api import router as bookings_router
app.include_router(bookings_router)
