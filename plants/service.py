from fastapi import Depends
from sqlalchemy.orm import Session, query

from schemas import ApiUser
from auth import get_current_user
from db import get_db

from plants.schemas import PlantCreate
from plants.models import Plant


async def create_plant(plant: PlantCreate,
                       db: Session = Depends(get_db),
                       user: ApiUser = Depends(get_current_user)):
    if user.auth_level >= 1:
        new_plant = Plant(
            name=plant.name,
            acquire_time=plant.acquire_time,
            is_alive=plant.is_alive,
            species=plant.species,
            watering_frequency=plant.watering_frequency,
            last_watering=plant.last_watering
        )
        db.add_all(new_plant)
        db.commit()

