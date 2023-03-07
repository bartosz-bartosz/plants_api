from fastapi import Depends
from sqlalchemy.orm import Session, query

from schemas import ApiUser
from auth import get_current_user
from db import get_db

from plants.schemas import PlantCreate
from plants.models import Plant


async def create_plant(plant: PlantCreate,
                       user: ApiUser,
                       db: Session):
    if user.auth_level >= 1:
        new_plant = Plant(
            owner_id=user.id,
            name=plant.name,
            acquire_time=plant.acquire_time,
            is_alive=plant.is_alive,
            species=plant.species,
            watering_frequency=plant.watering_frequency,
            last_watering=plant.last_watering
        )
        db.add(new_plant)
        db.commit()

        return new_plant
    return None


async def get_by_id(plant_id: int, db: Session):
    requested_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    return requested_plant


async def delete_by_id(plant_id: int, db: Session):
    deleted_item = db.query(Plant).filter(Plant.id == plant_id).delete()
    return deleted_item
