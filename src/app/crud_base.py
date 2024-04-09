from typing import Any, Dict, Generic, Iterable, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# noinspection PyTypeChecker
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, obj_id: Any) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == obj_id) # type: ignore
        return db.execute(query).scalar_one_or_none()

    def get_multi(self,
                  db: Session,
                  *,
                  skip: int = 0,
                  limit: int = 100,
                  filters: list | None = None,
                  **kwargs) -> Iterable[ModelType]:
        query = select(self.model)
        if kwargs.get("user_id"):
            filters = [self.model.user_id == kwargs["user_id"]] # pyright: ignore
        if filters:
            query = query.where(*filters)
        query = query.offset(skip).limit(limit)
        return db.execute(query).scalars().all() # pyright: ignore

    def create(self, db: Session, *, new_obj: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(new_obj)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self,
               db: Session,
               *,
               db_obj: ModelType,
               obj_in: UpdateSchemaType | Dict[str, Any]) -> ModelType: # pyright: ignore
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def delete(self, db: Session, *, obj_id: int) -> ModelType:
        query = select(self.model).where(self.model.id == obj_id) # pyright: ignore
        obj = db.execute(query).scalar_one_or_none()
        db.delete(obj)
        db.commit()
        return obj # pyright: ignore

    def get_rows_count(self, db: Session, ):
        count_query = func.count(self.model.id) # pyright: ignore
        return db.execute(count_query).scalar()
