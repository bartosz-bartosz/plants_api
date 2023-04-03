from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, Text, Float, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db import Base


class Plant(Base):
    """Basic model for plants table"""
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("api_users.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    acquire_time= mapped_column(DateTime)
    is_alive: Mapped[bool] = mapped_column(Integer)
    species: Mapped[str] = mapped_column(String, nullable=False)
    watering_frequency: Mapped[int] = mapped_column(Integer)
    last_watering = mapped_column(DateTime)


class Watering(Base):
    """Basic model for waterings table"""
    __tablename__ = "waterings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plant_id: Mapped[int] = mapped_column(Integer, ForeignKey("plants.id"))
    timestamp = mapped_column(DateTime, nullable=False)
    fertilizer: Mapped[bool] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("api_users.id"))


class PlantLogs(Base):
    """Table for storing plant logs from a microcontroller in the future
    needs plant_id foreign key"""
    __tablename__ = "plant_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp = mapped_column(DateTime)
    plant_name: Mapped[str] = mapped_column(String, nullable=False)
    moisture: Mapped[float] = mapped_column(Float, nullable=False)

