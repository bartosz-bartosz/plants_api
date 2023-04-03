from typing import Union, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ----------------------------------- FORM SCHEMAS
class PlantBase(BaseModel):
    name: str


class PlantCreate(PlantBase):
    acquire_time: Optional[datetime]
    is_alive: Optional[int] = 1
    species: Optional[str]
    watering_frequency: Optional[int]
    last_watering: Optional[datetime]


class PlantUpdate(PlantCreate):
    name: Optional[str]


class PlantLogCreate(BaseModel):
    timestamp: int
    plant_name: str
    moisture: float


# ----------------------------------- DATABASE MODELS
class PlantDB(PlantBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# ----------------------------------- RESPONSE MODELS
class Plant(PlantDB):
    pass
