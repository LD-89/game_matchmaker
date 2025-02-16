from functools import lru_cache

from redis.asyncio import ConnectionPool, Redis


@lru_cache
def get_redis_pool() -> ConnectionPool:
    return ConnectionPool.from_url(
        "redis://redis:6379/0",
        max_connections=1000,
        socket_keepalive=True,
        decode_responses=False
    )

class RedisClient:
    def __init__(self):
        self.pool: ConnectionPool = get_redis_pool()

        async def get_client(self) -> Redis:
            return Redis(connection_pool=self.pool)