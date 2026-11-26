from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.common.mixins import TimestampMixin
from config.database import Base

class Warehouse(Base, TimestampMixin):
    __tablename__ = "warehouses_warehouse"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_organization.id"), index=True)
    daily_limit: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"Warehouse id={self.id}, name={self.name}, organization_id={self.organization_id}"