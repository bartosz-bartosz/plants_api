from typing import Union, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ----------------------------------- FORM SCHEMAS
class PlantBase(BaseModel):
    name: str


class PlantCreate(PlantBase):
    user_id: int
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


class WateringBase:
    id: int


class WateringCreate(WateringBase):
    plant_id: int
    user_id: int
    timestamp: Optional[datetime]
    fertilizer: bool = Field(default=False)


class WateringUpdate(WateringBase):
    ...


# ----------------------------------- DATABASE MODELS
class PlantDB(PlantBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# ----------------------------------- RESPONSE MODELS


class Plant(PlantDB):
    pass
