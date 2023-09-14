from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.middlewares import set_middlewares
from src.routes import set_routes


def create_app(title: str, version: str, description: str) -> FastAPI:
    app = FastAPI(title=title, version=version, description=description, docs_url=None)

    app.mount("/static", StaticFiles(directory="static"), name="static")

    set_middlewares(app)
    set_routes(app)

    return app
