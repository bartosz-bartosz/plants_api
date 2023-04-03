from datetime import datetime
from typing import Mapping

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from auth import get_current_user
from schemas import ApiUser

from plants import service, models as m
from plants import crud
from plants.dependencies import valid_plant_id
from plants.schemas import PlantBase, PlantCreate, PlantLogCreate, Plant

# from plants.models import Plant


router = APIRouter(
    prefix="/plants",
    tags=['plants']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=PlantBase)
async def create_plant(plant_in: PlantCreate,
                       db: Session = Depends(get_db),
                       user: ApiUser = Depends(get_current_user)):
    plant = crud.plant.create(db=db, obj_in=plant_in)
    return plant


@router.get('/{plant_id}', status_code=status.HTTP_200_OK, response_model=Plant)
async def fetch_plant(plant_id: int,
                      db: Session = Depends(get_db),
                      current_api_user: ApiUser = Depends(get_current_user)):
    return crud.plant.get(db=db, obj_id=plant_id)


@router.put('/{plant_id}')
async def update_plant(db: Session = Depends(get_db),
                       current_api_user: ApiUser = Depends(get_current_user)):
    pass


@router.delete('/{plant_id}')
async def delete_plant(plant_id: int,
                       db: Session = Depends(get_db),
                       current_api_user: ApiUser = Depends(get_current_user)):
    return crud.plant.delete(db=db, obj_id=plant_id)


@router.get('')
async def read_plant_list(db: Session = Depends(get_db),
                          current_api_user: ApiUser = Depends(get_current_user)):
    if current_api_user.auth_level >= 1:
        return crud.plant.get_multi(db=db)


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
