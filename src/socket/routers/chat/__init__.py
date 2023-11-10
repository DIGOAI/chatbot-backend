from typing import Any

from socketio import ASGIApp, AsyncServer  # type: ignore

from src.socket.routers.chat.events import (
    FRONTEND_SEND_MESSAGE_EVENT,
    SERVER_NOTIFY_FRONTEND_NEW_MESSAGE_EVENT,
)


def router(app_with_sio: ASGIApp):
    namespace = "/chat"

    sio: AsyncServer = app_with_sio.sio  # type: ignore

    @sio.on(FRONTEND_SEND_MESSAGE_EVENT, namespace=namespace)  # type: ignore
    async def send_message(sid: Any, data: Any):  # type: ignore
        await sio.emit(SERVER_NOTIFY_FRONTEND_NEW_MESSAGE_EVENT, namespace=namespace, skip_sid=sid)  # type: ignore
