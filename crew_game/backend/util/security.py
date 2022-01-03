from datetime import datetime, timedelta

import pydantic
from jose import jwt
from passlib.context import CryptContext

from crew_game.backend import schemas, settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(sub: str, delta_min: str):
    delta = timedelta(delta_min)
    now = datetime.utcnow()
    expires = delta + now
    claims = {"exp": expires, "nbf": now, "sub": sub}
    encoded_jwt = jwt.encode(
        claims,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def create_access_token(username: str):
    return create_token(username, settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_register_token(email: str):
    return create_token(email, settings.REGISTER_TOKEN_EXPIRE_MINUTES)


def create_reset_token(email: str):
    return create_token(email, settings.RESET_TOKEN_EXPIRE_MINUTES)


def verify_token(token: str, exception: Exception):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenData(**payload)
        return token_data
    except (jwt.JWTError, pydantic.ValidationError):
        raise exception


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
