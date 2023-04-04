from crud_base import CRUDBase
from routers.plant.models import Plant
from routers.plant.schemas import PlantCreate, PlantUpdate


class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    ...


plant_crud = CRUDPlant(Plant)
