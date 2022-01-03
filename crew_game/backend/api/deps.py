from typing import Generator

import pydantic
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from crew_game.backend import schemas, settings
from crew_game.backend.database import crud, database, models

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_VERSION}/auth/access-token"
)


def get_db() -> Generator:
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenData(**payload)
    except (jwt.JWTError, pydantic.ValidationError):
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.sub)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
