from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from crew_game.backend import schemas, settings
from crew_game.backend.api import deps
from crew_game.backend.database import crud, models
from crew_game.backend.util import security

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
async def login_for_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud.get_user_by_username(db, form_data.username)
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


@router.post("/test-token", response_model=schemas.User)
async def test_token(current_user: models.User = Depends(deps.get_current_user)):
    return current_user


@router.post("/register", response_model=schemas.User)
async def register_user(
    db: Session = Depends(deps.get_db),
    username: str = Body(..., max_length=40),
    email: EmailStr = Body(...),
    password: str = Body(..., min_length=8, max_length=40),
):
    if not settings.ALLOW_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not accepting new registrations",
        )

    user = crud.get_user_by_username(db, username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requestd username is already in use",
        )

    user = crud.get_user_by_email(db, email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested email is already in use",
        )

    print(username, email, password)
    user_in = schemas.UserCreate(username=username, email=email, password=password)
    user = crud.create_user(db, user_in)

    return user


# TODO: recover-password
# TODO: reset-password
