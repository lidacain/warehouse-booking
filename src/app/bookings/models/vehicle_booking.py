import enum
from datetime import date
from sqlalchemy import Date, Enum, ForeignKey, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column
from app.common.mixins import TimestampMixin
from config.database import Base


class VehicleBooking(Base, TimestampMixin):
    __tablename__ = "bookings_vehicle_booking"
    __table_args__ = (
        Index(
            "bookings_vehicle_booking_active_vin_idx",
            "vin",
            unique=True,
            postgresql_where=text("status = 'ACTIVE'"),
        ),
    )

    class Status(enum.StrEnum):
        ACTIVE = "ACTIVE"
        CANCELLED = "CANCELLED"

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(String(17), index=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses_warehouse.id"), index=True)
    booking_date: Mapped[date] = mapped_column(Date)
    status: Mapped[Status] = mapped_column(
        Enum(Status, native_enum=False, length=20),
        default=Status.ACTIVE,
        server_default=Status.ACTIVE.value,
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations_organization.id"), index=True
    )

    def __repr__(self) -> str:
        return f"VehicleBooking id={self.id}, vin={self.vin}, status={self.status}"