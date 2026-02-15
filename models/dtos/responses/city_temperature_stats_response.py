from pydantic import BaseModel

from models.dtos.city_temperature_stats_cache_entry_dto import CityTemperatureStatsCacheEntryDto


class CityTemperatureStatsResponse(BaseModel):
    city_name: str
    min_temp: float
    max_temp: float
    avg_temp: float

    @classmethod
    def from_cache(cls, city_name: str, stats: CityTemperatureStatsCacheEntryDto) -> "CityTemperatureStatsResponse":
        return cls(
            city_name=city_name,
            min_temp=stats.min_temp,
            max_temp=stats.max_temp,
            avg_temp=stats.avg_temp,
        )
