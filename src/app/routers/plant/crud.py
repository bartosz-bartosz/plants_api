from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select, func, text, and_, or_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.crud_base import CRUDBase, ModelType
from app.routers.plant.models import Plant
from app.routers.plant.schemas import PlantCreate, PlantResponse, PlantUpdate
from app.utils import needs_watering


# noinspection PyTypeChecker
class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    def read_unwatered(
        self, db: Session, *, skip: int = 0, limit: int = 10, user_id: int
    ) -> List[Plant]:
        filters = [self.model.user_id == user_id]
        plants = super().get_multi(db=db, skip=skip, limit=limit, filters=filters)
        unwatered = [plant for plant in plants if needs_watering(plant.last_watering, plant.watering_frequency)]
        return unwatered

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, **kwargs
    ) -> List[PlantResponse]:
        if kwargs.get("user_id"):
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .where(self.model.user_id == kwargs["user_id"])
            )
            result = db.execute(query).scalars().all()
            return result
        return super().get_multi(db, skip=skip, limit=limit)


plant_crud = CRUDPlant(Plant)
