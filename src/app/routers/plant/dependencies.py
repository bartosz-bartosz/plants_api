from typing import Mapping

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.routers.plant.exceptions import PlantNotFound
from app.routers.plant.crud import plant_crud


async def valid_plant_id(plant_id: int,
                         db: Session = Depends(get_db)) -> Mapping:
    plant = await plant_crud.get(db=db, obj_id=plant_id)
    if not plant:
        raise PlantNotFound
    return plant
