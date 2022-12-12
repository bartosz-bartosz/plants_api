from pydantic import BaseModel


class ApiUser(BaseModel):
    __tablename__ = "api_users"
    
    username: str | None = None
    auth_level: int | None = None


