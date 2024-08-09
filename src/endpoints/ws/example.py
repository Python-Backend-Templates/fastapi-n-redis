import json

from fastapi import WebSocket, WebSocketDisconnect, Depends
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject
from websockets.exceptions import ConnectionClosed

from config.di import Container
from interfaces import IWebSocketManager
from utils.routing import APIRouter


router = APIRouter()


@router.websocket("/ping/{room_id}/")
@version(0)
@inject
async def rooms(
    websocket: WebSocket,
    room_id: str,
    manager: IWebSocketManager = Depends(Provide[Container.websocket_manager]),
):
    await manager.connect(websocket, room_id)
    await manager.send(
        room_id,
        json.dumps(
            {
                "room_id": room_id,
                "message": f"User connected to room - {room_id}",
            }
        ),
    )
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send(
                room_id, json.dumps({"room_id": room_id, "message": data})
            )
    except (WebSocketDisconnect, ConnectionClosed):
        await manager.send(
            room_id,
            json.dumps(
                {
                    "room_id": room_id,
                    "message": f"User disconnected from room - {room_id}",
                }
            ),
        )
    finally:
        await manager.disconnect(websocket, room_id)
