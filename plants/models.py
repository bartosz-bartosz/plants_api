from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, Text, Float
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship

from db import Base


class Plant(Base):
    """Basic model for plants table"""
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    acquire_time = Column(DATETIME)
    is_alive = Column(Integer)
    species = Column(String, nullable=False)
    watering_frequency = Column(Integer)
    last_watering = Column(DATETIME)


class PlantLogs(Base):
    """Table for storing plant logs from a microcontroller in the future"""
    __tablename__ = "plant_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DATETIME)
    plant_name = Column(String, nullable=False)
    moisture = Column(Float, nullable=False)
    