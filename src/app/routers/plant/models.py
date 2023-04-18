from sqlalchemy import Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.db import Base


class Plant(Base):
    """Basic model for plant table"""
    __tablename__ = "plant"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("api_users.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    acquire_time= mapped_column(DateTime)
    is_alive: Mapped[bool] = mapped_column(Integer)
    species: Mapped[str] = mapped_column(String, nullable=False)
    watering_frequency: Mapped[int] = mapped_column(Integer)
    last_watering = mapped_column(DateTime)

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

