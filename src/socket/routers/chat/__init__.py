from socketio import ASGIApp

from src.socket.routers.chat.events import (
    FRONTEND_SEND_MESSAGE_EVENT,
    SERVER_NOTIFY_FRONTEND_NEW_MESSAGE_EVENT,
)


def router(sio: ASGIApp):
    namespace = "/chat"

    @sio.on(FRONTEND_SEND_MESSAGE_EVENT, namespace=namespace)
    async def send_message(sid, data):
        await sio.emit(SERVER_NOTIFY_FRONTEND_NEW_MESSAGE_EVENT, namespace=namespace, skip_sid=sid)
