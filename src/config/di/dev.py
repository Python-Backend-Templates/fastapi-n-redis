from dependency_injector import containers, providers

from config import settings
from services import *


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["endpoints"], modules=[])

    redis_pubsub_manager = providers.Singleton(
        RedisPubSubManager,
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )
    websocket_manager = providers.Singleton(
        WebSocketManager, pubsub=redis_pubsub_manager
    )
