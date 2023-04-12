from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator, root_validator


# ----------------------------------- FORM SCHEMAS
class PlantBase(BaseModel):
    name: str


class PlantCreate(PlantBase):
    user_id: int
    acquire_time: Optional[datetime]
    is_alive: Optional[int | bool] = 1
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
        assert 2 <= len(v) <= 200, 'must be between 2 and 200 characters'
        return v

    @validator('is_alive')
    def is_alive_bool(cls, v):
        assert v in (0, 1, True, False), 'must be boolean, 0 or 1'
        return v

    @validator('species')
    def species_length(cls, v):
        assert 2 <= len(v) <= 200, 'must be between 2 and 200 characters'
        return v

    @validator('watering_frequency')
    def max_watering_frequency(cls, v):
        assert len(v) < 365, 'no plant can be watered so rarely!'
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
