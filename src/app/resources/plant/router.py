from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import app.resources.plant.models as models
from app.db import get_db
from app.resources.auth.auth import get_current_user
from app.resources.auth.schemas import ApiUser

from app.resources.plant import models as m
from app.resources.plant.crud import plant_crud
from app.resources.plant.schemas import (
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
    return await plant_crud.create(db=db, new_obj=plant_in)


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
    plant_obj = await plant_crud.get(db, plant_id)
    if not plant_obj:
        raise HTTPException(404, "Plant not found")
    return await plant_crud.update(db=db, db_obj=plant_obj, obj_in=update_data)


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
    return await plant_crud.read_unwatered(db=db, skip=skip, limit=limit, user_id=user.id)


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
    return await plant_crud.delete(db=db, obj_id=plant_id)
