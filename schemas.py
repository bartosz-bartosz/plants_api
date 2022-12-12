from pydantic import BaseModel


class ApiUser(BaseModel):
  
    username: str | None = None
    auth_level: int | None = None


