from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from auth import get_current_user, create_access_token, authenticate_user
from db import get_db
import schemas as m

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta()
    access_token = create_access_token(
        username = user.username, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
