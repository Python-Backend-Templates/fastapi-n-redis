from abc import ABC, abstractmethod

from fastapi import WebSocket
from redis import asyncio as aioredis
from redis.asyncio.client import PubSub


class IPubSubManager(ABC):
    @property
    @abstractmethod
    def connection(self) -> aioredis.Redis: ...
    @property
    @abstractmethod
    def pubsub(self) -> PubSub: ...
    @abstractmethod
    async def publish(self, channel: str, message: str) -> None: ...
    @abstractmethod
    async def subscribe(self, channel: str) -> None: ...
    @abstractmethod
    async def unsubscribe(self, channel: str) -> None: ...


class IWebSocketManager(ABC):
    @abstractmethod
    async def connect(self, websocket: WebSocket, room_id: str): ...
    @abstractmethod
    async def disconnect(self, websocket: WebSocket, room_id: str): ...
    @abstractmethod
    async def send(self, room_id: str, message: str) -> None: ...
    @abstractmethod
    async def event_listener(self, pubsub_subscriber): ...
