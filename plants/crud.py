from crud import CRUDBase
from plants.models import Plant, Watering
from plants.schemas import PlantCreate, PlantUpdate, WateringCreate, WateringUpdate


class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    ...


class CRUDWatering(CRUDBase[Watering, WateringCreate, WateringUpdate]):
    ...


plant = CRUDPlant(Plant)
watering = CRUDWatering(Watering)
