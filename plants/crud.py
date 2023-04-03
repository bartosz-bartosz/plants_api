from crud import CRUDBase
from plants.models import Plant, Watering
from plants.schemas import PlantCreate, PlantUpdate


class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    ...


class CRUDWatering(CRUDBase[Watering]):
    ...


plant = CRUDPlant(Plant)
watering = CRUDWatering(Watering)
