from datetime import datetime, timedelta
from typing import List, TYPE_CHECKING

from sqlalchemy import select, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, column_property, mapped_column, validates, relationship

from app.db import Base
from app.routers.watering.models import Watering

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
    species: Mapped[str] = mapped_column(String)
    watering_frequency: Mapped[int] = mapped_column(Integer)

    # relationships
    waterings: Mapped[List["Watering"]] = relationship("Watering", back_populates="plant")
    last_watering = column_property(select(Watering.timestamp) \
                                    .where(Watering.plant_id == id) \
                                    .order_by(Watering.timestamp.desc()).limit(1) \
                                    .scalar_subquery())

    @property
    def next_watering(self) -> datetime | None:
        if self.last_watering and self.watering_frequency:
            return self.last_watering + timedelta(days=self.watering_frequency)
        return None

    @property
    def days_left(self) -> int | None:
        if self.next_watering:
            return (self.next_watering - datetime.now()).days + 1
        return None

    @validates('name')
    def validate_name(self, key, value: str):
        if not 2 <= len(value) <= 200:
            raise ValueError("Name length must be between 2 and 200 characters")
        return value
