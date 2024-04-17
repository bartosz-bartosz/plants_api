from datetime import datetime, timedelta
from typing import List, TYPE_CHECKING

from sqlalchemy import select, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, column_property, mapped_column, validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.functions import concat
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql import func

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

    @hybrid_property
    def next_watering(self) -> datetime | None: # pyright: ignore
        if self.last_watering and self.watering_frequency:
            return self.last_watering + timedelta(days=self.watering_frequency)
        return None

    @next_watering.expression  # pyright: ignore
    @classmethod
    def next_watering(cls):
        print("expression")
        if cls.last_watering and cls.watering_frequency:
            return cls.last_watering + func.cast(concat(cls.watering_frequency, ' DAYS'), INTERVAL)
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
