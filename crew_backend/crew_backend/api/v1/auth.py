from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from crew_backend import mail, schemas, settings
from crew_backend.api import deps
from crew_backend.database import crud, models
from crew_backend.util import security

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
async def login_access_token(
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
    token_data = schemas.TokenData(sub=user.username, domain="access")
    access_token = security.create_token(
        token_data, settings.ACCESS_TOKEN_EXPIRE_MINUTES
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
            detail="Requested username is already in use",
        )

    user = crud.get_user_by_email(db, email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested email is already in use",
        )

    user_in = schemas.UserCreate(username=username, email=email, password=password)
    user = crud.create_user(db, user_in)

    token_data = schemas.TokenData(sub=user_in.email, domain="register")
    register_token = security.create_token(
        token_data, settings.REGISTER_TOKEN_EXPIRE_MINUTES
    )
    token_url = security.create_token_url(
        "v1/auth/confirm-registration", register_token
    )

    try:
        mail.send(
            to_addr=user_in.email,
            subject="New Account Registration: Welcome to Crew",
            template_name="new-account.jinja",
            data={
                "username": user_in.username,
                "email": user_in.email,
                "token_url": token_url,
            },
        )
    except mail.EmailError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send the registration email",
        )

    return user


@router.post("/test-email", response_model=schemas.Msg)
async def send_test_email():
    if not settings.TEST_EMAIL_ALLOWED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Test email API is diabled"
        )

    try:
        mail.send(
            to_addr=settings.TEST_EMAIL_ADDR,
            subject="Testing Email",
            template_name="test-email.jinja",
            data={"email": settings.TEST_EMAIL_ADDR},
        )
    except mail.EmailError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send the test email",
        )

    return {"msg": "Test Email Sent"}


@router.get("/confirm-registration", response_model=schemas.Msg)
async def confirm_registration(
    db: Session = Depends(deps.get_db),
    token: str = Query(...),
):
    token_data = security.verify_token(token, "register")
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify token"
        )

    user = crud.get_user_by_email(db, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.is_active = True
    db.commit()

    return {"msg": "Account registration confirmed"}


# TODO: recover-password
# TODO: reset-password
