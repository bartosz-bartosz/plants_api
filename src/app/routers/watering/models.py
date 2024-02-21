from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy.types import Boolean, SmallInteger

from app.db import Base

if TYPE_CHECKING:
    from app.routers.plant.models import Plant


class Watering(Base):
    """Basic model for watering table"""

    __tablename__ = "waterings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plant_id: Mapped[int] = mapped_column(Integer, ForeignKey("plants.id"))
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    fertilizer: Mapped[int] = mapped_column(SmallInteger)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("api_users.id"))

    # relationships
    plant: Mapped["Plant"] = relationship("Plant", back_populates="waterings")

    @validates("id")
    def validate_id(self, key, value: int):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer")
        return value

    @validates("plant_id")
    def validate_plant_id(self, key, value: int):
        if not isinstance(value, int):
            raise ValueError("Plant ID must be an integer")
        return value

    @validates("timestamp")
    def validate_timestamp(self, key, value: datetime):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
            except (ValueError, TypeError):
                raise ValueError("Incorrect datetime format")
        return value

    @validates("fertilizer")
    def validate_fertilizer(self, key, value: int):
        if not isinstance(value, int):
            raise ValueError("Fertilizer must be an integer")
        return value

    @validates("user_id")
    def validate_user_id(self, key, value: int):
        if not isinstance(value, int):
            raise ValueError("User ID must be an integer")
        return value
