from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ApiUser(Base):
    __tablename__ = "api_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    auth_level: Mapped[str] = mapped_column(Integer)
