from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from app.crud_base import CRUDBase
from app.routers.plant.models import Plant
from app.routers.plant.schemas import PlantCreate, PlantUpdate


# noinspection PyTypeChecker
class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):

    def read_unwatered(self, db: Session, *, skip: int = 0, limit: int = 100, local_datetime: datetime) -> List[Plant]:
        current_time = db.query(func.now())
        query = select(self.model).offset(skip).limit(limit) \
            .where(self.model.last_watering is not None) \
            .where(self.model.last_watering == func.date_sub(current_time, text(f"INTERVAL {self.model.watering_frequency} DAY")))

        return db.execute(query).scalars().all()


plant_crud = CRUDPlant(Plant)
