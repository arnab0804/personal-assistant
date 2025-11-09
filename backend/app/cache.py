import redis.asyncio as redis
from typing import Optional, Any
import json
from app.config import settings


_redis_client: Optional[redis.Redis] = None




async def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client




async def cache_get(key: str) -> Optional[Any]:
    """Get value from cache"""
    client = await get_redis()
    value = await client.get(key)
    if value:
        return json.loads(value)
    return None




async def cache_set(key: str, value: Any, ttl: int = settings.REDIS_CACHE_TTL) -> bool:
    """Set value in cache with TTL"""
    client = await get_redis()
    serialized = json.dumps(value)
    return await client.setex(key, ttl, serialized)




async def cache_delete(key: str) -> bool:
    """Delete value from cache"""
    client = await get_redis()
    return await client.delete(key) > 0




async def cache_clear_pattern(pattern: str) -> int:
    """Clear all keys matching pattern"""
    client = await get_redis()
    keys = await client.keys(pattern)
    if keys:
        return await client.delete(*keys)
    return 0




async def close_redis():
    """Close Redis connection"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()