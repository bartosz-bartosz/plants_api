from src.app.crud_base import CRUDBase
from src.app.routers.plant.models import Plant
from src.app.routers.plant.schemas import PlantCreate, PlantUpdate


class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    ...


plant_crud = CRUDPlant(Plant)
