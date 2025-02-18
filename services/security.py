from redis.commands.core import AsyncScript

from app.main import app
from config.redis import RedisClient

SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block"
}

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers.update(SECURITY_HEADERS)
    return response

RATE_LIMIT_SCRIPT = """
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local requests = tonumber(ARGV[3])
local now = tonumber(ARGV[4])

local remaining = capacity - requests
if remaining < 0 then
    return {remaining=0, reset=window}
end

redis.call('HINCRBY', key, 'count', requests)
redis.call('EXPIRE', key, window)
return {remaining=remaining, reset=window}
"""

class RateLimiter:
    def __init__(self):
        self.redis = RedisClient()
        self.script = AsyncScript(None, RATE_LIMIT_SCRIPT)

    async def check_limit(self, identifier: str) -> bool:
        async with await self.redis.get_client() as client:
            result = await self.script(
                keys=[f"rate_limit:{identifier}"],
                args=[100, 60, 1, int(time.time())],
                client=client
            )
            return result["remaining"] > 0