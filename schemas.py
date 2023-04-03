from typing import Union
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class ApiUser(BaseModel):
    id: Union[int, None] = None
    username: Union[str, None] = None
    auth_level: Union[int, None] = None


class ApiUserSignup(ApiUser):
    password: Union[str, None] = None


# ------------------------------------- RESPONSE MODELS
class ApiUserSafeResponse(ApiUser):
    username: str
    auth_level: int
    id: int

