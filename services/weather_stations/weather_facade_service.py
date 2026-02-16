from fastapi import HTTPException

from models.dtos import CityTemperatureStatsCacheEntryDto
from models.dtos.responses import CityTemperatureStatsResponse, CityAverageTemperatureResponse
from services.data_processing import DataProcessingService
from services.weather_stations import WeatherCachingService
from services.weather_stations.helpers.constants import OPERATORS


class WeatherFacadeService:

    def __init__(self, data_processing_service: DataProcessingService, weather_caching_service: WeatherCachingService):
        self._data_processing_service = data_processing_service
        self._weather_caching_service = weather_caching_service

    async def get_city(self, city_name: str) -> CityTemperatureStatsResponse:
        if await self._is_file_modified():
            await self._load_and_cache_stats()

        city_entry = await self._weather_caching_service.get_by_city(city_name)
        if not city_entry:
            raise HTTPException(status_code=404, detail=f"{city_name} city not found!")

        return CityTemperatureStatsResponse.from_cache(city_name, city_entry)

    async def list_all_cities(self) -> list[CityTemperatureStatsResponse]:
        city_entries = await self._get_stats_with_auto_reload()

        return [
            CityTemperatureStatsResponse.from_cache(city_name, city_stats)
            for city_name, city_stats in sorted(city_entries.items())
        ]

    async def filter_by_average_temperature(
            self, reference_temp: float, operator: str
    ) -> list[CityAverageTemperatureResponse]:
        city_entries = await self._get_stats_with_auto_reload()

        compare = OPERATORS.get(operator)
        if not compare:
            raise HTTPException(status_code=400, detail=f"Invalid operator: {operator}")

        return [
            CityAverageTemperatureResponse.from_cache(city_name, city_stats)
            for city_name, city_stats in sorted(city_entries.items())
            if compare(city_stats.avg_temp, reference_temp)
        ]

    async def reload_stats(self):
        await self._load_and_cache_stats()

    async def load_and_cache_on_startup(self) -> None:
        await self._load_and_cache_stats()

    async def clear_cache(self) -> None:
        await self._weather_caching_service.clear_cache()

    async def _load_and_cache_stats(self) -> dict[str, CityTemperatureStatsCacheEntryDto]:
        stats = self._data_processing_service.load_data_and_calculate_stats()
        mtime = self._data_processing_service.get_file_modified_time()

        await self._weather_caching_service.write_temperature_stats(stats)
        await self._weather_caching_service.set_file_mtime(mtime)

        return stats

    async def _is_file_modified(self) -> bool:
        current_mtime = self._data_processing_service.get_file_modified_time()
        cached_mtime = await self._weather_caching_service.get_file_mtime()

        if cached_mtime is None:
            return True
        return current_mtime > cached_mtime

    async def _get_stats_with_auto_reload(self) -> dict[str, CityTemperatureStatsCacheEntryDto]:
        if await self._is_file_modified():
            print("[auto-reload] CSV file changed, reloading stats...")
            return await self._load_and_cache_stats()

        city_entries = await self._weather_caching_service.get_all()
        if city_entries is None:
            return await self._load_and_cache_stats()

        return city_entries
