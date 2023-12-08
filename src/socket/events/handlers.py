from typing import Any

from socketio import AsyncServer  # type: ignore

from src.socket.events import SIOEvent


def set_event_handlers(app: AsyncServer):

    @app.on(SIOEvent.CLIENT_SEND_MESSAGE)  # type: ignore
    async def send_message(sid: Any, data: Any):  # type: ignore
        await app.emit(SIOEvent.SERVER_NOTIFY_FRONTEND, skip_sid=sid)  # type: ignore
