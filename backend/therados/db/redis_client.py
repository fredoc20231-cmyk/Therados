import redis.asyncio as redis
from typing import Optional
from therados.config.settings import settings
import logging

logger = logging.getLogger("therados.db.redis")

class RedisClient:
    def __init__(self) -> None:
        self._client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        try:
            self._client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            await self._client.ping()
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Ephemeral caching disabled.")

    async def close(self) -> None:
        if self._client:
            await self._client.close()

    async def get(self, key: str) -> Optional[str]:
        if not self._client:
            return None
        try:
            val = await self._client.get(key)
            return str(val) if val is not None else None
        except Exception:
            return None

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        if not self._client:
            return False
        try:
            await self._client.set(key, value, ex=ex)
            return True
        except Exception:
            return False

redis_client = RedisClient()
