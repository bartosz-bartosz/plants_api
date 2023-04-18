from app.crud_base import CRUDBase
from app.routers.plant.models import Plant
from app.routers.plant.schemas import PlantCreate, PlantUpdate


class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    ...


plant_crud = CRUDPlant(Plant)
