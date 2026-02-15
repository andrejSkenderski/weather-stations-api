from pydantic import BaseModel


class CityTemperatureStatsCacheEntryDto(BaseModel):
    min_temp: float
    max_temp: float
    avg_temp: float
