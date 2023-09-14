from fastapi import FastAPI as _FastAPI
from fastapi.middleware.cors import CORSMiddleware as _CORS

from src.config import Config as _Config
from src.middlewares.error_handler import ErrorHandler as _ErrorHandler
from src.middlewares.jwt_bearer import JWTBearer

__all__ = [
    "JWTBearer",
]

_ORIGINS = _Config.ALLOWED_ORIGINS


def set_middlewares(app: _FastAPI):
    app.add_middleware(
        _CORS,
        allow_origins=_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.add_middleware(_ErrorHandler)
