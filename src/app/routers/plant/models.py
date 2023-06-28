from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.routers.watering.models import Watering


class Plant(Base):
    """Basic model for plant table"""
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("api_users.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    acquire_time= mapped_column(DateTime)
    is_alive: Mapped[bool] = mapped_column(Integer)
    species: Mapped[str] = mapped_column(String, nullable=False)
    watering_frequency: Mapped[int] = mapped_column(Integer)

    # relationships
    waterings: Mapped[List["Watering"]] = relationship("Watering", back_populates="plant")

    @property
    def last_watering(self) -> DateTime | None:
        if not self.waterings:
            return None
        return sorted([watering_time.timestamp for watering_time in self.waterings])[0]

    @validates('name')
    def validate_name(self, key, value: str):
        if not 2 <= len(value) <= 200:
            raise ValueError("Name length must be between 2 and 200 characters")
        return value


class PlantLogs(Base):
    """Table for storing plant logs from a microcontroller in the future
    needs plant_id foreign key"""
    __tablename__ = "plant_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp = mapped_column(DateTime)
    plant_name: Mapped[str] = mapped_column(String, nullable=False)
    moisture: Mapped[float] = mapped_column(Float, nullable=False)
