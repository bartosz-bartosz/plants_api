from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select, func, text, and_, or_
from sqlalchemy.orm import Session, selectinload

from app.crud_base import CRUDBase, ModelType
from app.routers.plant.models import Plant
from app.routers.plant.schemas import PlantCreate, PlantUpdate


# noinspection PyTypeChecker
class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    def read_unwatered(
        self, db: Session, *, skip: int = 0, limit: int = 10
    ) -> List[Plant]:
        plants = super().get_multi(db=db, skip=skip, limit=limit)

        return plants

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, **kwargs
    ) -> List[Plant]:
        if kwargs.get("user_id"):
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .where(self.model.user_id == kwargs["user_id"])
            )
            result = db.execute(query).scalars().all()
            for plant in result:
                plant.next_watering = (
                    plant.last_watering + timedelta(days=plant.watering_frequency)
                    if plant.last_watering
                    else None
                )
                plant.days_left = (
                    (plant.next_watering - datetime.now()).days
                    if plant.last_watering
                    else None
                )
                print(plant.__dict__)
            result = sorted(
                result,
                key=lambda x: x.days_left if x.days_left is not None else float("inf"),
            )
            return result
        return super().get_multi(db, skip=skip, limit=limit)


plant_crud = CRUDPlant(Plant)
