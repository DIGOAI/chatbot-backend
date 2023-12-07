from typing import Any

from socketio import AsyncServer  # type: ignore

from src.socket.events import events as sio_events


def set_events(app: AsyncServer):

    @app.on(sio_events.CLIENT_SEND_MESSAGE)  # type: ignore
    async def send_message(sid: Any, data: Any):  # type: ignore
        await app.emit(sio_events.SERVER_NOTIFY_FRONTEND, skip_sid=sid)  # type: ignore
