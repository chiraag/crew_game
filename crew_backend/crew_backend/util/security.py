from datetime import datetime, timedelta
from typing import Optional

import pydantic
from jose import jwt
from passlib.context import CryptContext

from crew_backend import schemas, settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(token_data: schemas.TokenData, delta_min: str) -> str:
    delta = timedelta(delta_min)
    now = datetime.utcnow()
    expires = delta + now
    claims = {"exp": expires, "nbf": now}
    claims.update(token_data.dict())
    encoded_jwt = jwt.encode(
        claims,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def create_token_url(endpoint: str, token: str) -> str:
    return f"{settings.BASE_URL}/{endpoint}?token={token}"


def verify_token(token: str, domain: str) -> Optional[schemas.TokenData]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenData(**payload)
        if token_data.domain == domain:
            return token_data
        else:
            return None
    except (jwt.JWTError, pydantic.ValidationError):
        return None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
