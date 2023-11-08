from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def apply_cors_middleware(app: FastAPI) -> FastAPI:
    """Applies CORS middleware"""
    origins = "*"
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app