from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, field_validator

from app.routers.watering.models import Watering


# ----------------------------------- FORM SCHEMAS
class PlantBase(BaseModel):
    name: str


class PlantCreate(PlantBase):
    user_id: int
    acquire_time: Optional[datetime | date]
    is_alive: Optional[int | bool] = 1
    species: Optional[str] = None
    watering_frequency: Optional[int]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
            date: lambda v: v.strftime("%Y-%m-%d"),
        }

    @field_validator("name")
    def username_length(cls, v):
        assert 2 <= len(v) <= 200, "must be between 2 and 200 characters"
        return v

    @field_validator("is_alive")
    def is_alive_bool(cls, v):
        assert v in (0, 1, True, False), "must be boolean, 0 or 1"
        return v

    @field_validator("species")
    def species_length(cls, v):
        if v:
            assert 2 <= len(v) <= 200, "must be between 2 and 200 characters"
        return v

    @field_validator("watering_frequency")
    def max_watering_frequency(cls, v):
        assert v < 365, "no plant can be watered so rarely!"
        return v


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
        from_attributes = True


# ----------------------------------- RESPONSE MODELS
class PlantResponse(PlantDB):
    species: Optional[str]
    watering_frequency: Optional[int]
    last_watering: Optional[datetime]
    next_watering: Optional[datetime]
    days_left: Optional[int]


class PlantResponseWater(PlantResponse):
    needs_water: Optional[bool]
