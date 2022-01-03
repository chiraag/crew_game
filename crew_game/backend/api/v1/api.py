from fastapi import APIRouter

from crew_game.backend.api.v1 import auth, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
