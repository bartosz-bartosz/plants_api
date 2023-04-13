from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel, validator


class WateringBase(BaseModel):
    ...


class WateringCreate(WateringBase):
    plant_id: int
    user_id: int
    timestamp: Optional[datetime]
    fertilizer: bool = Field(default=False)

    @validator('plant_id')
    def validate_plant_id(cls, v):
        assert v > 0
        return v

    @validator('user_id')
    def validate_user_id(cls, v):
        assert v > 0
        return v


class WateringUpdate(WateringBase):
    ...


class WateringQuerySchema(WateringBase):
    """ to do """
    ...
