from typing import Union
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class ApiUser(BaseModel):
    id: int
    username: str
    auth_level: int


class ApiUserSignup(BaseModel):
    username: str
    password: str


# ------------------------------------- RESPONSE MODELS
class ApiUserSafeResponse(BaseModel):
    username: str
    auth_level: int
    id: int
