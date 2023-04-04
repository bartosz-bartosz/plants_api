from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel


class WateringBase(BaseModel):
    id: int


class WateringCreate(WateringBase):
    plant_id: int
    user_id: int
    timestamp: Optional[datetime]
    fertilizer: bool = Field(default=False)


class WateringUpdate(WateringBase):
    ...


class WateringQuerySchema(WateringBase):
    """ to do """
    ...
