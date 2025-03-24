import json
from redis import Redis
from app.config import settings

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

class CacheService:
    CACHE_TTL = 120  # 2 minutes in seconds

    @staticmethod
    def get_cache_key(netuid: int, hotkey: str) -> str:
        return f"dividend:{netuid}:{hotkey}"

    @staticmethod
    def store_in_cache(netuid: int, hotkey: str, data: dict):
        """Store data in Redis cache"""
        key = CacheService.get_cache_key(netuid, hotkey)
        redis_client.setex(
            key,
            CacheService.CACHE_TTL,
            json.dumps(data)
        )

    @staticmethod
    def get_from_cache(netuid: int, hotkey: str) -> dict:
        """Retrieve data from Redis cache"""
        key = CacheService.get_cache_key(netuid, hotkey)
        data = redis_client.get(key)
        return json.loads(data) if data else None

async def set_cache(key: str, value: str, expiration: int = 3600):
    return redis_client.setex(key, expiration, value)

async def get_cache(key: str):
    return redis_client.get(key) 