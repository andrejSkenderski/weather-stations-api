from pydantic import BaseModel

from models.dtos.city_temperature_stats_cache_entry_dto import CityTemperatureStatsCacheEntryDto


class CityAverageTemperatureResponse(BaseModel):
    city_name: str
    avg_temp: float

    @classmethod
    def from_cache(cls, city_name: str, stats: CityTemperatureStatsCacheEntryDto) -> "CityAverageTemperatureResponse":
        return cls(
            city_name=city_name,
            avg_temp=stats.avg_temp,
        )
