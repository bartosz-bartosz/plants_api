from fastapi import Depends, FastAPI

from auth import get_current_user
import models as m

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/me")
async def read_users_me(current_user: m.User = Depends(get_current_user)):
    return current_user
