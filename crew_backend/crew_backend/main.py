from fastapi import FastAPI

from crew_backend.api.v1.api import api_router
from crew_backend.settings import API_VERSION

app = FastAPI()
app.include_router(api_router, prefix=f"/{API_VERSION}")


@app.get("/")
async def root():
    return f"Welcome to Crew Backend {API_VERSION}"
