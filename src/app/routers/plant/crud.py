from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud_base import CRUDBase
from app.routers.plant.models import Plant
from app.routers.plant.schemas import PlantCreate, PlantResponse, PlantUpdate
from app.utils import needs_watering


# noinspection PyTypeChecker
class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    def read_unwatered(self,
                       db: Session,
                       *,
                       skip: int = 0,
                       limit: int = 10,
                       user_id: int) -> List[Plant]:
        plants = super().get_multi(db=db, skip=skip, limit=limit, user_id=user_id)
        unwatered = [plant for plant in plants if needs_watering(plant.last_watering, plant.watering_frequency)]
        return unwatered

plant_crud = CRUDPlant(Plant)
