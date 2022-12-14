from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ApiUser(BaseModel):
    username: str | None = None
    auth_level: int | None = None


class ApiUserSignup(ApiUser):
    password: str | None = None
    
    
# PLANTS

class PlantLog(BaseModel):
    timestamp: int
    plant_name: str
    moisture: float

