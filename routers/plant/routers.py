from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from auth import get_current_user
from schemas import ApiUser

from routers.plant import models as m
from routers.plant import crud
from routers.plant.schemas import PlantBase, PlantCreate, PlantUpdate, PlantLogCreate, Plant

# from plant.models import Plant


router = APIRouter(
    prefix="/plant",
    tags=['plant']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=PlantBase)
async def create_plant(plant_in: PlantCreate,
                       db: Session = Depends(get_db),
                       user: ApiUser = Depends(get_current_user)):
    plant_in.user_id = user.id
    plant = crud.plant.create(db=db, new_obj=plant_in)
    return plant.__dict__


@router.get('/{plant_id}', status_code=status.HTTP_200_OK, response_model=Plant)
async def fetch_plant(plant_id: int,
                      db: Session = Depends(get_db),
                      current_api_user: ApiUser = Depends(get_current_user)):
    plant = crud.plant.get(db=db, obj_id=plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found.")
    return crud.plant.get(db=db, obj_id=plant_id)


@router.put('/{plant_id}')
async def update_plant(plant_id: int, update_data: PlantUpdate,
                       db: Session = Depends(get_db),
                       current_api_user: ApiUser = Depends(get_current_user)):
    crud.plant.update(db=db, db_obj=crud.plant.get(db, plant_id), obj_in=update_data)
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
