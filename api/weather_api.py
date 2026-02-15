from typing import Literal

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query, HTTPException

from api.auth_api import verify_token
from config.container import Container
from models.dtos.responses import CityTemperatureStatsResponse, CityAverageTemperatureResponse
from services.weather_stations import WeatherFacadeService

Operator = Literal["lt", "gt", "eq", "lte", "gte"]

weather_api = APIRouter(prefix="/weather", tags=["Weather"])


@weather_api.get("/cities", response_model=list[CityTemperatureStatsResponse],
                 summary="List all cities with respective temperature statistics")
@inject
async def list_all_city_stats(
        _token: dict = Depends(verify_token),
        service: WeatherFacadeService = Depends(Provide[Container.weather_facade_service]),
):
    return await service.list_all_cities()


@weather_api.get("/city", response_model=CityTemperatureStatsResponse, summary="Get temperature stats for a city")
@inject
async def get_city_stats(
        name: str = Query(min_length=1),
        _token: dict = Depends(verify_token),
        service: WeatherFacadeService = Depends(Provide[Container.weather_facade_service]),
):
    return await service.get_city(name)


@weather_api.get("/averages/{reference_temp}", response_model=list[CityAverageTemperatureResponse],
                 summary="Filter cities by average temperature")
@inject
async def filter_cities_by_avg_temp(
        reference_temp: float,
        operator: Operator = Query(description="Comparison: lt, gt, eq, lte, gte"),
        _token: dict = Depends(verify_token),
        service: WeatherFacadeService = Depends(Provide[Container.weather_facade_service]),
):
    return await service.filter_by_average_temperature(reference_temp, operator)


@weather_api.post("/reload", summary="Manual data reload from CSV")
@inject
async def reload_stats(
        _token: dict = Depends(verify_token),
        service: WeatherFacadeService = Depends(Provide[Container.weather_facade_service]),
):
    await service.reload_stats()
    return {"message": "City stats reloaded successfully"}


@weather_api.post("/clear_cache", summary="Clear cache for development purposes")
@inject
async def clear_cache(
        _token: dict = Depends(verify_token),
        service: WeatherFacadeService = Depends(Provide[Container.weather_facade_service]),
):
    await service.clear_cache()
    return {"message": "Cache cleared successfully"}
