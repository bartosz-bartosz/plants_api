from typing import List

from sqlalchemy import select, func
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

    def read_count(self, db: Session, user_id: int) -> int:
        query = select(func.count(self.model.id)).where(self.model.user_id == user_id)
        result = db.execute(query).scalar()
        if not result:
            return 0
        return result

plant_crud = CRUDPlant(Plant)
