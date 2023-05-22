from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.routers.auth.auth import get_current_user
from app.routers.auth.schemas import ApiUser

from app.routers.watering.crud import watering_crud
from app.routers.watering.schemas import WateringBase, WateringCreate, WateringUpdate, WateringQuerySchema

watering_router = APIRouter(
    prefix="/watering",
    tags=['watering']
)


@watering_router.post('', status_code=status.HTTP_200_OK, response_model=WateringBase)
async def create_watering(watering_in: WateringCreate,
                          db: Session = Depends(get_db),
                          user: ApiUser = Depends(get_current_user)):
    watering_in.user_id = user.id
    watering = watering_crud.create(db=db, new_obj=watering_in)
    return watering.__dict__


@watering_router.get('/{watering_id}', status_code=status.HTTP_200_OK)
async def get_item(watering_id: int,
                   db: Session = Depends(get_db),
                   user: ApiUser = Depends(get_current_user)):
    return watering_crud.get(db=db, obj_id=watering_id)


@watering_router.get('', status_code=status.HTTP_200_OK)
async def get_list(watering_filters: WateringQuerySchema,
                   db: Session = Depends(get_db),
                   user: ApiUser = Depends(get_current_user)):
    if user.auth_level >= 1:
        return watering_crud.get_multi(db=db)


@watering_router.patch("/{watering_id}", status_code=status.HTTP_200_OK, response_model=WateringBase)
async def update_item(watering_id: int, watering_data: WateringUpdate,
                      db: Session = Depends(get_db),
                      user: ApiUser = Depends(get_current_user)):
    return watering_crud.update(db=db, db_obj=watering_crud.get(db=db, obj_id=watering_id), obj_in=watering_data)


@watering_router.delete("/watering_id", status_code=status.HTTP_200_OK)
async def delete_item(watering_id: int,
                      db: Session = Depends(get_db),
                      user: ApiUser = Depends(get_current_user)):
    return watering_crud.delete(db=db, obj_id=watering_id)
