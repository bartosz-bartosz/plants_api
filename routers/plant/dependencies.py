from typing import Mapping

from fastapi import Depends
from sqlalchemy.orm import Session

from db import get_db
from routers.plant.exceptions import PlantNotFound


async def valid_plant_id(plant_id: int,
                         db: Session = Depends(get_db)) -> Mapping:
    plant = await service.get_by_id(plant_id, db)
    if not plant:
        raise PlantNotFound
    return plant
