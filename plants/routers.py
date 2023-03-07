from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from auth import get_current_user
from schemas import ApiUser

from plants import service, models as m
from plants.schemas import PlantCreate, PlantLogCreate

router = APIRouter(
    prefix="/plants",
    tags=['plants']
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_plant(plant_data: PlantCreate,
                       db: Session = Depends(get_db),
                       user: ApiUser = Depends(get_current_user)):
    plant = await service.create_plant(plant_data, user, db)
    return "plant created i hope"


@router.get('/{id}')
async def read_plant(db: Session = Depends(get_db),
                     current_api_user: ApiUser = Depends(get_current_user)):
    pass


@router.put('/{id}')
async def update_plant(db: Session = Depends(get_db),
                       current_api_user: ApiUser = Depends(get_current_user)):
    pass


@router.delete('/{id}')
async def delete_plant(db: Session = Depends(get_db),
                       current_api_user: ApiUser = Depends(get_current_user)):
    pass


@router.get('')
async def read_plant_list(db: Session = Depends(get_db),
                          current_api_user: ApiUser = Depends(get_current_user)):
    if current_api_user.auth_level >= 1:
        pass


@router.post("/log")
async def create_plant_log(form_data: PlantLogCreate,
                           db: Session = Depends(get_db),
                           current_api_user: ApiUser = Depends(get_current_user)):
    if current_api_user.auth_level >= 1:
        timestamp = datetime.fromtimestamp(form_data.timestamp)
        plant_log = m.PlantLogs(timestamp=timestamp,
                                plant_name=form_data.plant_name,
                                moisture=form_data.moisture)

        db.add(plant_log)
        db.commit()
        db.refresh(plant_log)

        return plant_log
