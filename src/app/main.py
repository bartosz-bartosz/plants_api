from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.routers.plant.router import plant_router
from app.routers.watering.router import watering_router
from app.routers.auth.auth import get_current_user, create_access_token, authenticate_user, get_password_hash
from app.db import get_db
from app.routers.auth import models as m, schemas as sc

app = FastAPI()

app.include_router(plant_router)
app.include_router(watering_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/token", response_model=sc.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
   
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta()
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=sc.ApiUserSafeResponse)
async def read_users_me(current_user: m.ApiUser = Depends(get_current_user)):
    return current_user.__dict__


@app.post("/users/create-api-user")
async def create_api_user(form_data: sc.ApiUserSignup, db: Session = Depends(get_db)):
    api_user = db.query(m.ApiUser).filter(m.ApiUser.username == form_data.username).first()
    if api_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    else:
        hashed_password = get_password_hash(form_data.password)
        new_api_user = m.ApiUser(username=form_data.username,
                                 hashed_password=hashed_password,
                                 auth_level=1)
        db.add(new_api_user)
        db.commit()
        db.refresh()
        
        return new_api_user