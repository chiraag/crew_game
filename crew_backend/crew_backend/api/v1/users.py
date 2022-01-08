from fastapi import APIRouter, Depends

from crew_backend.api.deps import get_current_active_user
from crew_backend.schemas.user import User

router = APIRouter()


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# TODO: update user email, password
