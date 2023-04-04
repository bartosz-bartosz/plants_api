from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Watering(Base):
    """Basic model for watering table"""
    __tablename__ = "watering"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plant_id: Mapped[int] = mapped_column(Integer, ForeignKey("plant.id"))
    timestamp = mapped_column(DateTime, nullable=False)
    fertilizer: Mapped[bool] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("api_users.id"))
