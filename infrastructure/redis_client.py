import redis.asyncio as redis


class RedisClient:

    def __init__(self, url: str):
        self.client = redis.from_url(
            url,
            decode_responses=True,
            max_connections=20,
        )

    async def ping(self) -> bool:
        return await self.client.ping()

    async def close(self):
        await self.client.aclose()

    async def get(self, key: str) -> str | None:
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl: int = None) -> None:
        await self.client.set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)
