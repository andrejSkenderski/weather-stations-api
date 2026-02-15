from contextlib import asynccontextmanager

from dependency_injector.wiring import wire
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import weather_api as weather_api_module
from api import auth_api as auth_api_module
from api.root import register_api
from config.container import Container
from config.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):

    container: Container = app.state.container

    # STARTUP
    redis = container.redis()

    await redis.ping()
    print("[startup] Redis connected")

    weather_facade_service = container.weather_facade_service()
    await weather_facade_service.load_and_cache_on_startup()
    print("[startup] City stats loaded and cached")

    print("[startup] Ready to serve requests")
    yield

    # SHUTDOWN
    print("[shutdown] Closing connections...")
    await redis.close()
    print("[shutdown] All connections closed")


def create_app() -> FastAPI:
    settings = Settings()

    container = Container()
    container.config.redis_url.from_value(settings.redis_url)
    container.config.secret_key.from_value(settings.secret_key)
    container.config.valid_username.from_value(settings.valid_username)
    container.config.valid_password.from_value(settings.valid_password)
    container.config.algorithm.from_value(settings.algorithm)
    container.config.access_token_expire_minutes.from_value(settings.access_token_expire_minutes)
    container.config.csv_file_path.from_value(settings.csv_file_path)

    wire(modules=[weather_api_module, auth_api_module], container=container)

    app = FastAPI(
        title="Weather Stations API",
        description="FastAPI + Redis",
        version="1.0.0",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    app.state.container = container

    register_api(app)
    return app
