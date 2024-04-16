from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.routers.auth.auth import get_current_user
from app.routers.auth.schemas import ApiUser

from app.routers.plant import models as m
from app.routers.plant.crud import plant_crud
from app.routers.plant.schemas import (
    PlantCreate,
    PlantUpdate,
    PlantLogCreate,
    PlantCreateDB,
    PlantResponse,
    PlantResponseWater,
)

plant_router = APIRouter(prefix="/plant", tags=["plant"])


""" ---------------- POST """


@plant_router.post("", status_code=status.HTTP_201_CREATED, response_model=PlantCreate)
async def create_plant(
    plant_create: PlantCreate,
    db: Session = Depends(get_db),
    user: ApiUser = Depends(get_current_user),
):
    """Creates a new plant in the database"""
    if user.auth_level < 1:
        return HTTPException(status_code=403, detail="Forbidden")
    plant_in = PlantCreateDB(**plant_create.model_dump(), user_id=user.id)
    return plant_crud.create(db=db, new_obj=plant_in)


""" ---------------- PUT """


@plant_router.put("/{plant_id}", response_model=PlantResponse)
async def update_plant(
    plant_id: int,
    update_data: PlantUpdate,
    db: Session = Depends(get_db),
    current_api_user: ApiUser = Depends(get_current_user),
):
    """Updates a plant in the database by ID"""
    if current_api_user.auth_level < 1:
        return HTTPException(status_code=403, detail="Forbidden")
    plant_obj = plant_crud.get(db, plant_id)
    plant_crud.update(db=db, db_obj=plant_obj, obj_in=update_data)
    return plant_crud.get(db=db, obj_id=plant_id)


""" ---------------- GET  """


@plant_router.get("/count", status_code=status.HTTP_200_OK)
async def read_plants_count(
    db: Session = Depends(get_db), current_api_user: ApiUser = Depends(get_current_user)
):
    """Reads the count of all user plants in the database"""
    if current_api_user.auth_level < 1:
        return HTTPException(status_code=403, detail="Forbidden")
    count = await plant_crud.read_count(db=db, user_id=current_api_user.id)
    return {"count": count}


@plant_router.get(
    "/list", status_code=status.HTTP_200_OK, response_model=List[PlantResponse]
)
async def read_plant_list(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "last_watering",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_api_user: ApiUser = Depends(get_current_user),
):
    """Reads all user plants from the database"""
    if current_api_user.auth_level < 1:
        return HTTPException(status_code=403, detail="Forbidden")
    response = await plant_crud.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        user_id=current_api_user.id,
    )
    return response


@plant_router.get(
    "/unwatered",
    status_code=status.HTTP_200_OK,
    response_model=List[PlantResponseWater],
)
async def read_unwatered_plants(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: ApiUser = Depends(get_current_user),
):
    """Reads only these user plants that should have already been watered by now."""
    if user.auth_level < 1:
        return HTTPException(status_code=403, detail="Forbidden")
    return plant_crud.read_unwatered(db=db, skip=skip, limit=limit, user_id=user.id)


@plant_router.get(
    "/{plant_id}", status_code=status.HTTP_200_OK, response_model=PlantResponse
)
async def read_plant(
    plant_id: int,
    db: Session = Depends(get_db),
    current_api_user: ApiUser = Depends(get_current_user),
):
    """Reads a single plant from the database by ID"""
    if current_api_user.auth_level < 1:
        return HTTPException(status_code=403, detail="Forbidden")
    plant = await plant_crud.get(db=db, obj_id=plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found.")
    if plant.user_id != current_api_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return plant


""" ---------------- DELETE """


@plant_router.delete("/{plant_id}")
async def delete_plant(
    plant_id: int,
    db: Session = Depends(get_db),
    current_api_user: ApiUser = Depends(get_current_user),
):
    """Deletes a plant from the database by ID"""
    if current_api_user.auth_level < 1:
        return HTTPException(status_code=403, detail="Forbidden")
    return plant_crud.delete(db=db, obj_id=plant_id)


#  MISC
@plant_router.post("/log")
async def create_plant_log(
    form_data: PlantLogCreate,
    db: Session = Depends(get_db),
    current_api_user: ApiUser = Depends(get_current_user),
):
    """This endpoint is just a placeholder, in the future 'logs' endpoints should have their own directory"""
    if current_api_user.auth_level >= 1:
        timestamp = datetime.fromtimestamp(form_data.timestamp)
        plant_log = m.PlantLogs(
            timestamp=timestamp,
            plant_name=form_data.plant_name,
            moisture=form_data.moisture,
        )
        db.add(plant_log)
        db.commit()
        db.refresh(plant_log)
        return plant_log
