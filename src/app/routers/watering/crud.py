from src.app.crud_base import CRUDBase
from src.app.routers.watering.models import Watering
from src.app.routers.watering.schemas import WateringCreate, WateringUpdate


class CRUDWatering(CRUDBase[Watering, WateringCreate, WateringUpdate]):
    ...


watering_crud = CRUDWatering(Watering)
