from enum import Enum
from typing import NotRequired, TypedDict

from fastapi import APIRouter, FastAPI

from src.api.routes.auth_routes import router as auth_router
from src.api.routes.client_routes import router as client_router
from src.api.routes.conversation_routes import router as conversation_router
from src.api.routes.email_routes import router as email_router

#
# from src.api.routes.external_routes import router as external_router
from src.api.routes.message_routes import router as message_router
from src.api.routes.root_routes import router as root_router
from src.api.routes.ticket_routes import router as tickets_router
from src.api.routes.twilio_routes import router as twilio_router


class _RoutesType(TypedDict):
    router: APIRouter
    prefix: NotRequired[str]


class _APIVersion(str, Enum):
    v1 = "v1"


_default_prefix = f"/api/{_APIVersion.v1.value}"

_routes: list[_RoutesType] = [
    {"router": root_router},
    {"router": auth_router, "prefix": _default_prefix},
    {"router": client_router, "prefix": _default_prefix},
    {"router": message_router, "prefix": _default_prefix},
    {"router": conversation_router, "prefix": _default_prefix},
    {"router": twilio_router, "prefix": _default_prefix},
    {"router": tickets_router, "prefix": _default_prefix},
    {"router": email_router, "prefix": _default_prefix},
]


def set_routes(app: FastAPI) -> None:
    for route in _routes:
        app.include_router(**route)
