import aioredis

from . import settings


class RedisPool:
    def __init__(self, url):
        self.url = url
        self.pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await aioredis.create_redis_pool(
                self.url, minsize=5, maxsize=10
            )

    async def disconnect(self):
        await self.pool.close()
        self.pool = None

PUB_SUB = RedisPool(settings.Redis.PUB_SUB_URL)