from typing import Tuple

from utils.routing import APIRoute
from utils.decorators import apply_tags


@apply_tags(("HTTP",))
def get_routers() -> Tuple[APIRoute]:
    from .example import router as example_router

    return (example_router,)
