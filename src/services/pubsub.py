from redis import asyncio as aioredis
from redis.asyncio.client import PubSub

from interfaces import IPubSubManager


class RedisPubSubManager(IPubSubManager):
    _connection: aioredis.Redis | None = None
    _pubsub: PubSub | None = None

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @property
    def connection(self) -> aioredis.Redis:
        if self._connection is None:
            self._connection = aioredis.Redis(
                host=self.host,
                port=self.port,
                auto_close_connection_pool=False,
            )
        return self._connection

    @property
    def pubsub(self) -> PubSub:
        if self._pubsub is None:
            self._pubsub = self.connection.pubsub()
        return self._pubsub

    async def publish(self, channel: str, message: str) -> None:
        await self.connection.publish(channel, message)

    async def subscribe(self, channel: str) -> None:
        await self.pubsub.subscribe(channel)

    async def unsubscribe(self, channel: str) -> None:
        await self.pubsub.unsubscribe(channel)
