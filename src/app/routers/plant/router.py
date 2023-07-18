from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.routers.auth.auth import get_current_user
from app.routers.auth.schemas import ApiUser

from app.routers.plant import models as m
from app.routers.plant.crud import plant_crud
from app.routers.plant.schemas import PlantBase, PlantCreate, PlantUpdate, PlantLogCreate, PlantResponse


plant_router = APIRouter(
    prefix="/plant",
    tags=['plant']
)


#  BASIC CRUD
@plant_router.post('', status_code=status.HTTP_201_CREATED, response_model=PlantBase)
async def create_plant(plant_in: PlantCreate,
                       db: Session = Depends(get_db),
                       user: ApiUser = Depends(get_current_user)):
    plant_in.user_id = user.id
    plant = plant_crud.create(db=db, new_obj=plant_in)
    return plant.__dict__


@plant_router.get('/{plant_id}', status_code=status.HTTP_200_OK, response_model=PlantResponse)
async def read_plant(plant_id: int,
                      db: Session = Depends(get_db),
                      current_api_user: ApiUser = Depends(get_current_user)):
    plant = plant_crud.get(db=db, obj_id=plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found.")
    return plant_crud.get(db=db, obj_id=plant_id)


@plant_router.put('/{plant_id}', response_model=PlantResponse)
async def update_plant(plant_id: int, update_data: PlantUpdate,
                       db: Session = Depends(get_db),
                       current_api_user: ApiUser = Depends(get_current_user)):
    plant_obj = plant_crud.get(db, plant_id)
    plant_crud.update(db=db, db_obj=plant_obj, obj_in=update_data)
    return plant_crud.get(db=db, obj_id=plant_id)


@plant_router.delete('/{plant_id}')
async def delete_plant(plant_id: int,
                       db: Session = Depends(get_db),
                       current_api_user: ApiUser = Depends(get_current_user)):
    if current_api_user.auth_level <= 1:
        raise
    return plant_crud.delete(db=db, obj_id=plant_id)


@plant_router.get('', status_code=status.HTTP_200_OK, response_model=List[PlantResponse])
async def read_plant_list(skip: int = 0, limit: int = 10,
                          db: Session = Depends(get_db),
                          current_api_user: ApiUser = Depends(get_current_user)):
    if current_api_user.auth_level >= 1:
        return plant_crud.get_multi(db=db, skip=skip, limit=limit)


#  USE SPECIFIC ENDPOINTS
@plant_router.get('/unwatered', status_code=status.HTTP_200_OK, response_model=List[PlantResponse])
async def read_unwatered_plants(skip: int = 0, limit: int = 10,
                                db: Session = Depends(get_db),
                                current_api_user: ApiUser = Depends(get_current_user)):
    if current_api_user.auth_level >= 1:
        return plant_crud.read_unwatered(db=db, skip=skip, limit=limit)


#  MISC
@plant_router.post("/log")
async def create_plant_log(form_data: PlantLogCreate,
                           db: Session = Depends(get_db),
                           current_api_user: ApiUser = Depends(get_current_user)):
    """ This endpoint is just a placeholder, in the future 'logs' endpoints should have their own directory """
    if current_api_user.auth_level >= 1:
        timestamp = datetime.fromtimestamp(form_data.timestamp)
        plant_log = m.PlantLogs(timestamp=timestamp,
                                plant_name=form_data.plant_name,
                                moisture=form_data.moisture)

        db.add(plant_log)
        db.commit()
        db.refresh(plant_log)

        return plant_log
