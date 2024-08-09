from typing import Tuple

from utils.routing import APIRouter


def get_routers() -> Tuple[APIRouter]:
    from .http import get_routers as get_http_routers

    return (*get_http_routers(),)


def get_ws_routers() -> Tuple[APIRouter]:
    from .ws import get_routers as get_ws_routers

    return (*get_ws_routers(),)
