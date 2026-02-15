from dependency_injector import containers, providers

from infrastructure.redis_client import RedisClient
from services.auth import JwtAuthenticator
from services.data_processing import DataProcessingService
from services.weather_stations import WeatherCachingService, WeatherFacadeService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    config = providers.Configuration()

    # INFRASTRUCTURE

    redis = providers.Singleton(
        RedisClient,
        url=config.redis_url,
    )

    # SERVICES

    jwt_auth = providers.Singleton(
        JwtAuthenticator,
        secret_key=config.secret_key,
        valid_username=config.valid_username,
        valid_password=config.valid_password,
        algorithm=config.algorithm,
        access_token_expire_minutes=config.access_token_expire_minutes,
    )

    weather_caching_service = providers.Factory(
        WeatherCachingService,
        redis=redis,
    )

    data_processing_service = providers.Factory(
        DataProcessingService,
        csv_file_path=config.csv_file_path,
    )

    weather_facade_service = providers.Factory(
        WeatherFacadeService,
        data_processing_service=data_processing_service,
        weather_caching_service=weather_caching_service,
    )
