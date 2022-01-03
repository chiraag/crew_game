from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from crew_game.backend import schemas, settings
from crew_game.backend.api import deps
from crew_game.backend.database import crud
from crew_game.backend.util import security

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
async def login_for_access_token(
    db: dict = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud.get_user_fake(db, form_data.username)
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
