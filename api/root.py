from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.auth_api import auth_api
from api.weather_api import weather_api


def register_api(app: FastAPI):
    api = APIRouter(prefix="/api", tags=["API"])

    api.include_router(weather_api)
    api.include_router(auth_api)

    app.include_router(api)
