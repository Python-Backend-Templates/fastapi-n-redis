import asyncio
from typing import Dict, List

from fastapi import WebSocket
from redis.asyncio.client import PubSub

from interfaces import IPubSubManager, IWebSocketManager


class WebSocketManager(IWebSocketManager):
    def __init__(self, pubsub: IPubSubManager):
        self.pubsub = pubsub
        self.rooms: Dict[str, List[WebSocket]] = dict()
        self.event_listener_task = None

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()

        if room_id in self.rooms:
            self.rooms[room_id].append(websocket)
        else:
            self.rooms[room_id] = [websocket]
            await self.pubsub.subscribe(room_id)

        if self.event_listener_task is None:
            self.event_listener_task = asyncio.create_task(
                self.event_listener(self.pubsub.pubsub)
            )

    async def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.rooms:
            self.rooms[room_id].remove(websocket)

        if room_id not in self.rooms or not self.rooms[room_id]:
            self.rooms.pop(room_id, None)
            await self.pubsub.unsubscribe(room_id)

    async def send(self, room_id: str, message: str) -> None:
        await self.pubsub.publish(room_id, message)

    async def event_listener(self, subscriber: PubSub):
        while True:
            message = await subscriber.get_message(ignore_subscribe_messages=True)
            if message is None:
                continue
            room_id = message["channel"].decode("utf-8")
            sockets = self.rooms[room_id]
            for socket in sockets:
                await socket.send_text(message["data"].decode("utf-8"))
