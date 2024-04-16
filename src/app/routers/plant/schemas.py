from typing import Optional, List
from datetime import datetime, date, timedelta
from pydantic import BaseModel, ConfigDict, field_validator, computed_field


# ----------------------------------- FORM SCHEMAS
class PlantBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class PlantCreate(PlantBase):
    acquire_time: Optional[datetime | date]
    is_alive: Optional[int | bool] = 1
    species: Optional[str] = None
    watering_frequency: Optional[int]

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


class PlantCreateDB(PlantCreate):
    user_id: int


class PlantUpdate(BaseModel):
    name: Optional[str] = None
    acquire_time: Optional[datetime | date] = None
    is_alive: Optional[int | bool] = None
    species: Optional[str] = None
    watering_frequency: Optional[int] = None


class PlantLogCreate(BaseModel):
    timestamp: int
    plant_name: str
    moisture: float


# ----------------------------------- DATABASE MODELS
class PlantDB(PlantBase):
    id: int


# ----------------------------------- RESPONSE MODELS
class PlantResponse(PlantDB):
    species: Optional[str]
    watering_frequency: Optional[int]
    last_watering: Optional[datetime]
    next_watering: Optional[datetime]
    days_left: Optional[int]

    # @computed_field
    # @property
    # def next_watering(self) -> datetime | None:
    #     if self.last_watering and self.watering_frequency:
    #         return self.last_watering + timedelta(days=self.watering_frequency)
    #     return None

    # @computed_field
    # @property
    # def days_left(self) -> int | None:
    #     if self.next_watering:
    #         return (self.next_watering - datetime.now()).days
    #     return None


class PlantResponseWater(PlantResponse):
    pass
