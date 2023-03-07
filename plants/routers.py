from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from auth import get_current_user
from schemas import ApiUser

from . import models as m
from .schemas import PlantCreate, PlantLog

router = APIRouter(
    prefix="/plants",
    tags=['plants']
)


@router.post('/plant')
async def create_plant(form_data: PlantCreate,
                       db: Session = Depends(get_db),
                       current_api_user: ApiUser = Depends(get_current_user)):
    if current_api_user.auth_level >= 1:
        pass


@router.get('/plant')
async def read_plant_list(db: Session = Depends(get_db),
                          current_api_user: ApiUser = Depends(get_current_user)):
    if current_api_user.auth_level >= 1:
        pass


@router.post("/plant_log")
async def create_plant_log(form_data: PlantLog,
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
