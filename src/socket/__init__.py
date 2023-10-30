import socketio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


def socketio_mount(
    app: FastAPI,
    async_mode: str = "asgi",
    mount_path: str = "/socket.io/",
    socketio_path: str = "socket.io",
    logger: bool = False,
    engineio_logger: bool = False,
    cors_allowed_origins="*",
    **kwargs
) -> FastAPI:
    """Mounts a SocketIO server over a FastAPI app."""
    sio = socketio.AsyncServer(async_mode=async_mode,
                               cors_allowed_origins=cors_allowed_origins,
                               logger=logger,
                               engineio_logger=engineio_logger, **kwargs)
    sio_app = socketio.ASGIApp(sio, socketio_path=socketio_path)

    # mount
    app.add_route(mount_path, route=sio_app, methods=["GET", "POST"])
    app.add_websocket_route(mount_path, sio_app)

    return app
