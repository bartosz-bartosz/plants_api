from crud import CRUDBase
from routers.plant.models import Plant
from routers.plant.schemas import PlantCreate, PlantUpdate


class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    ...

plant = CRUDPlant(Plant)
