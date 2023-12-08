from socketio import AsyncServer  # type: ignore

from src.socket.events import SIOEvent, handlers
from src.socket.socket_server import FastAPIWithSIO, SocketServer

__all__ = [
    "create_socket",
    "FastAPIWithSIO",
    "SIOEvent",
    "SocketServer",
]


def create_socket(async_mode: str = "asgi", cors_allowed_origins: str | list[str] = "*"):
    """Mounts an async SocketIO app over an FastAPI app."""

    app = AsyncServer(async_mode=async_mode, cors_allowed_origins=cors_allowed_origins)
    handlers.set_event_handlers(app)

    return app
