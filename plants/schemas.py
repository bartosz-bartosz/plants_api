from typing import Union, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PlantCreate(BaseModel):
    name: str
    acquire_time: Optional[datetime]
    species: Optional[str]
    watering_frequency: Optional[int]
    last_watering: Optional[datetime]


class PlantLogCreate(BaseModel):
    timestamp: int
    plant_name: str
    moisture: float
