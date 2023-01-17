from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, Text, Float
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship

from db import Base


class ApiUser(Base):
    __tablename__ = "api_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    auth_level = Column(Integer)


class PlantLogs(Base):
    __tablename__ = "plant_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DATETIME)
    plant_name = Column(String, nullable=False)
    moisture = Column(Float, nullable=False)
    
    
class Plants(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    acquire_time = Column(DATETIME)
    is_alive = Column(Integer)
    species = Column(String, nullable=False)
    watering_frequency = Column(Integer)
    last_watering = Column(DATETIME)
        