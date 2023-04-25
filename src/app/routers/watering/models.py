from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.routers.plant.models import Plant


class Watering(Base):
    """Basic model for watering table"""
    __tablename__ = "waterings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plant_id: Mapped[int] = mapped_column(Integer, ForeignKey("plants.id"))
    timestamp = mapped_column(DateTime, nullable=False)
    fertilizer: Mapped[bool] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("api_users.id"))

    # relationships
    plant: Mapped["Plant"] = relationship("Plant", back_populates="waterings")

    @validates('timestamp')
    def validate_timestamp(self, key, value):
        if not type(value) == datetime:
            raise ValueError('Incorrect datetime format')
        return value
