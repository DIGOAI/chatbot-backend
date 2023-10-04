from fastapi import FastAPI as _FastAPI
from fastapi.middleware.cors import CORSMiddleware as _CORS

from src.api.middlewares.auth_apitoken import APITokenAuth
from src.api.middlewares.error_handler import ErrorHandler as _ErrorHandler
from src.api.middlewares.jwt_bearer import JWTBearer
from src.api.middlewares.logger_handler import LoggerHandler as _LoggerHandler
from src.config import Config as _Config

__all__ = [
    "JWTBearer",
    "APITokenAuth",
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
    app.add_middleware(_LoggerHandler)
