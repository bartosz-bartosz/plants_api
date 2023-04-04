from crud_base import CRUDBase
from routers.watering.models import Watering
from routers.watering.schemas import WateringCreate, WateringUpdate


class CRUDWatering(CRUDBase[Watering, WateringCreate, WateringUpdate]):
    ...


watering_crud = CRUDWatering(Watering)
