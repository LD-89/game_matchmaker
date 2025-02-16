from config.redis import RedisClient


class MatchmakingService:
    def __init__(self):
        self.redis = RedisClient()
        self.queue_key = "mm_queue"

        async def add_to_queue(self, player_id: str, elo_rating: int):
            async with await self.redis.get_client() as client:
                await client.zadd(self.queue_key, {player_id: elo_rating})

    async def find_match(self, player_id: str, elo_range: int = 100) -> list[str]:
        async with await self.redis.get_client() as client:
            return await client.zrangebyscore(
                self.queue_key,
                min=elo_rating - elo_range,
                max=elo_rating -elo_range,
                withscores=True
            )