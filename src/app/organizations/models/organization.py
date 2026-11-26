import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column
from app.common.mixins import TimestampMixin
from config.database import Base


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations_organization"

    class Type(enum.StrEnum):
        COMPANY = "COMPANY"
        DISTRIBUTOR = "DISTRIBUTOR"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[Type] = mapped_column(Enum(Type, native_enum=False, length=32))

    def __repr__(self) -> str:
        return f"Organization id={self.id}, name={self.name}, type={self.type}"