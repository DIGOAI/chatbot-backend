from enum import Enum
from typing import NotRequired, TypedDict

from fastapi import APIRouter, FastAPI

from src.routes.root_routes import router as root_router
from src.routes.user_routes import router as user_router


class _RoutesType(TypedDict):
    router: APIRouter
    prefix: NotRequired[str]


class _APIVersion(str, Enum):
    v1 = "v1"


_default_prefix = f"/api/{_APIVersion.v1.value}" + "/{company}"

_routes: list[_RoutesType] = [
    {"router": root_router},
    {"router": user_router, "prefix": _default_prefix}
]


def set_routes(app: FastAPI) -> None:
    for route in _routes:
        app.include_router(**route)
