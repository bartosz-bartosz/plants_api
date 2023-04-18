from app.crud_base import CRUDBase
from app.routers.watering.models import Watering
from app.routers.watering.schemas import WateringCreate, WateringUpdate


class CRUDWatering(CRUDBase[Watering, WateringCreate, WateringUpdate]):
    ...


watering_crud = CRUDWatering(Watering)
