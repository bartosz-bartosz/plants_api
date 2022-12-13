from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship

from db import Base


class ApiUser(Base):
    __tablename__ = "api_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    auth_level = Column(Integer)
