from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field, BaseModel, field_validator


class WateringBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WateringCreate(WateringBase):
    plant_id: int
    timestamp: Optional[datetime]
    fertilizer: int = Field(default=0, ge=0, le=1)

    @field_validator("plant_id")
    def validate_plant_id(cls, v):
        assert v > 0
        return v


class WateringUpdate(WateringBase):
    ...


class WateringQuerySchema(WateringBase):
    """to do"""

    ...
