from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from auth import get_current_user
import models as m
import schemas as sc


router = APIRouter(
    prefix="/plants",
    tags=['plants']
)


@router.post("/add_log")
async def add_plant_log(form_data: sc.PlantLog,
                        db: Session = Depends(get_db),
                        current_api_user: sc.ApiUser = Depends(get_current_user)):

    if current_api_user.auth_level == 1:
        timestamp = datetime.fromtimestamp(form_data.timestamp)
        plant_log = m.PlantLogs(timestamp=timestamp,
                                plant_name=form_data.plant_name,
                                moisture=form_data.moisture)
        
        db.add(plant_log)
        db.commit()
        db.refresh(plant_log)
        
        return plant_log
    