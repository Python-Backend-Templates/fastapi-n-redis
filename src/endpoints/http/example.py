import json

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from interfaces import IPubSubManager
from utils.routing import APIRouter


router = APIRouter(prefix="/example")


@router.post("/ping/{room_id}/", status_code=200)
@version(0)
@inject
async def ping(
    room_id: str,
    pubsub: IPubSubManager = Depends(Provide[Container.redis_pubsub_manager]),
):
    await pubsub.publish(room_id, json.dumps({"message": "pong", "room_id": room_id}))
    return JSONResponse({"message": "pong", "room_id": room_id}, status_code=200)
