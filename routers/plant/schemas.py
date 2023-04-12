from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator, root_validator


# ----------------------------------- FORM SCHEMAS
class PlantBase(BaseModel):
    name: str


class PlantCreate(PlantBase):
    # TODO date format to be specified correctly/validated
    user_id: int
    acquire_time: Optional[datetime]
    is_alive: Optional[int] = 1
    species: Optional[str]
    watering_frequency: Optional[int]
    last_watering: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

    @validator('name')
    def username_length(cls, v):
        assert 0 < len(v) < 200, 'must be between 1 and 200 characters'
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
        orm_mode = True


# ----------------------------------- RESPONSE MODELS


class Plant(PlantDB):
    pass
