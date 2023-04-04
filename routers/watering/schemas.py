from datetime import datetime
from typing import Optional

from pydantic import Field


class WateringBase:
    id: int


class WateringCreate(WateringBase):
    plant_id: int
    user_id: int
    timestamp: Optional[datetime]
    fertilizer: bool = Field(default=False)


class WateringUpdate(WateringBase):
    ...
