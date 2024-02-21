from typing import Union
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ApiUser(BaseModel):
    id: int | None = None
    username: str | None = None
    auth_level: int | None = None


class ApiUserSignup(BaseModel):
    username: str | None = None
    password: str | None = None


# ------------------------------------- RESPONSE MODELS
class ApiUserSafeResponse(BaseModel):
    username: str
    auth_level: int
    id: int
