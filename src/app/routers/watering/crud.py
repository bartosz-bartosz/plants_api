from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud_base import CRUDBase, ModelType
from app.routers.watering.models import Watering
from app.routers.watering.schemas import WateringCreate, WateringUpdate


# noinspection PyTypeChecker
class CRUDWatering(CRUDBase[Watering, WateringCreate, WateringUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, **kwargs) -> List[ModelType]:
        if kwargs.get('plant_id'):
            query = select(self.model).offset(skip).limit(limit).where(self.model.plant_id == kwargs['plant_id'])
            return db.execute(query).scalars().all()
        return super().get_multi(db, skip=skip, limit=limit)


watering_crud = CRUDWatering(Watering)
