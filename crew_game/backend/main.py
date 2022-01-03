from fastapi import FastAPI

from crew_game.backend.api.v1.api import api_router
from crew_game.backend.settings import API_VERSION

app = FastAPI()
app.include_router(api_router, prefix=f"/{API_VERSION}")


@app.get("/")
async def root():
    return f"Welcome to Crew Backend {API_VERSION}"
