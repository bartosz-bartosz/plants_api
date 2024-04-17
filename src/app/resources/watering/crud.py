from typing import Iterable, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud_base import CRUDBase, ModelType
from app.resources.watering.models import Watering
from app.resources.watering.schemas import (
    WateringCreateDB,
    WateringUpdate,
)


# noinspection PyTypeChecker
class CRUDWatering(CRUDBase[Watering, WateringCreateDB, WateringUpdate]):
    async def get_multi(self,
                  db: Session,
                  *,
                  skip: int = 0,
                  limit: int = 100,
                  **kwargs) -> Iterable[Watering]:
        if kwargs.get("plant_id"):
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .where(self.model.plant_id == kwargs["plant_id"])
            )
            return db.execute(query).scalars().all()
        return await super().get_multi(db, skip=skip, limit=limit)


watering_crud = CRUDWatering(Watering)
