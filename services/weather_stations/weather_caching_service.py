import orjson

from infrastructure.redis_client import RedisClient
from models.dtos import CityTemperatureStatsCacheEntryDto
from services.weather_stations.helpers.constants import CACHE_KEY_PREFIX, FILE_MTIME_KEY


class WeatherCachingService:

    def __init__(self, redis: RedisClient):
        self._redis = redis

    async def get_by_city(self, city: str) -> CityTemperatureStatsCacheEntryDto | None:
        key = self._build_key(city)
        cached = await self._redis.get(key)
        if not cached:
            return None
        return CityTemperatureStatsCacheEntryDto(**orjson.loads(cached))

    async def write_temperature_stats(self, stats: dict[str, CityTemperatureStatsCacheEntryDto]) -> None:
        for city, stat in stats.items():
            key = self._build_key(city)
            await self._redis.client.set(key, orjson.dumps(stat.model_dump()).decode())

    async def get_all(self) -> dict[str, CityTemperatureStatsCacheEntryDto] | None:
        keys = []
        async for key in self._redis.client.scan_iter(match=f"{CACHE_KEY_PREFIX}*"):
            keys.append(key)

        if not keys:
            return None

        values = await self._redis.client.mget(keys)

        result = {}
        for key, value in zip(keys, values):
            if value:
                city = key.replace(CACHE_KEY_PREFIX, "")
                result[city] = CityTemperatureStatsCacheEntryDto(**orjson.loads(value))

        return result if result else None

    async def set_file_mtime(self, mtime: float) -> None:
        await self._redis.client.set(FILE_MTIME_KEY, str(mtime))

    async def get_file_mtime(self) -> float | None:
        mtime = await self._redis.get(FILE_MTIME_KEY)
        return float(mtime) if mtime else None

    async def clear_cache(self) -> None:
        await self._redis.client.flushdb()

    @staticmethod
    def _build_key(city: str) -> str:
        return f"{CACHE_KEY_PREFIX}{city}"
