from typing import Any

from fastapi import FastAPI
from socketio import ASGIApp, AsyncServer  # type: ignore

from src.socket.routers import router as socketio_router_v1


class FastAPIWithSIO(ASGIApp):

    sio: AsyncServer  # type: ignore

    def __init__(self,  socketio_server, other_asgi_app=None,  # type: ignore
                 static_files=None, socketio_path='socket.io',  # type: ignore
                 on_startup=None, on_shutdown=None):  # type: ignore
        super().__init__(socketio_server, other_asgi_app, static_files=static_files,  # type: ignore
                         socketio_path=socketio_path, on_startup=on_startup,
                         on_shutdown=on_shutdown)


def socketio_mount(
    app: FastAPI,
    async_mode: str = "asgi",
    mount_path: str = "/socket.io/",
    socketio_path: str = "socket.io",
    logger: bool = False,
    engineio_logger: bool = False,
    cors_allowed_origins: str | list[str] = "*",
    **kwargs: Any
):
    """Mounts an async SocketIO app over an FastAPI app."""

    sio = AsyncServer(async_mode=async_mode,
                      cors_allowed_origins=cors_allowed_origins,
                      logger=logger,
                      engineio_logger=engineio_logger,
                      **kwargs
                      )

    # sio_app = ASGIApp(sio, socketio_path=socketio_path)

    sio_app = FastAPIWithSIO(sio, socketio_path=socketio_path)
    sio_app.sio = sio

    # mount
    app.add_route(mount_path, route=sio_app, methods=["GET", "POST"], include_in_schema=False)  # type: ignore
    app.add_websocket_route(mount_path, route=sio_app)  # type: ignore

    socketio_router_v1(sio_app)

    return sio_app
