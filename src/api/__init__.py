from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.context import lifespan
from src.api.middlewares import set_middlewares
from src.api.routes import set_routes
from src.api.version import __VERSION__


def create_app(title: str, version: str, description: str) -> FastAPI:
    app = FastAPI(title=title, version=version, description=description, docs_url=None, lifespan=lifespan)

    app.mount("/static", StaticFiles(directory="src/api/static"), name="static")

    set_middlewares(app)
    set_routes(app)

    return app


__all__ = ["create_app", "__VERSION__"]
