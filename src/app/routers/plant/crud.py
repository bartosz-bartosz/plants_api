from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select, func, text, and_, or_
from sqlalchemy.orm import Session, selectinload

from app.crud_base import CRUDBase, ModelType
from app.routers.plant.models import Plant
from app.routers.plant.schemas import PlantCreate, PlantUpdate


# noinspection PyTypeChecker
class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):

    def read_unwatered_test(self, db: Session, *, skip: int = 0, limit: int = 10) -> List[Plant]:
        """ This method doesn't work correctly, as it has no access to `last_watering` which is defined as a `waterings` relationship/property"""
        query = select(self.model).offset(skip).limit(limit)\
            .options(selectinload(self.model.waterings))\
            .where(and_(self.model.last_watering >= func.date_sub(func.now(), text(f"INTERVAL plants.watering_frequency DAY")),
                        self.model.last_watering is not None))

        print(query)

        return db.execute(query).scalars().all()

    def read_unwatered(self, db: Session, *, skip: int = 0, limit: int = 10) -> List[Plant]:
        plants = super().get_multi(db=db, skip=skip, limit=limit)
        for plant in plants:
            plant.needs_water = plant.last_watering <= datetime.now() - timedelta(days=plant.watering_frequency) if plant.last_watering is not None else True

        return plants

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, **kwargs) -> List[ModelType]:
        if kwargs.get('user_id'):
            query = select(self.model).offset(skip).limit(limit).where(self.model.user_id == kwargs['user_id'])
            result = db.execute(query).scalars().all()
            for plant in result:
                plant.next_watering = plant.last_watering + timedelta(days=plant.watering_frequency) if plant.last_watering else None
                plant.days_left = (plant.next_watering - datetime.now()).days if plant.last_watering else None
                print(plant.__dict__)
            result = sorted(result, key=lambda x: x.days_left if x.days_left is not None else float('inf'))
            return result
        return super().get_multi(db, skip=skip, limit=limit)


plant_crud = CRUDPlant(Plant)
