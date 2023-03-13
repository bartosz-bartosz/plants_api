from crud import CRUDBase
from plants.models import Plant
from plants.schemas import PlantCreate, PlantUpdate


class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    ...


plant = CRUDPlant(Plant)
