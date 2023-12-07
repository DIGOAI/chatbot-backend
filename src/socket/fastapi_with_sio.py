from fastapi import FastAPI
from socketio import ASGIApp, AsyncServer  # type: ignore


class FastAPIWithSIO(ASGIApp):

    def __init__(self,  socketio_server: AsyncServer, other_asgi_app: FastAPI | None = None, socketio_path: str = 'socket.io'):
        self.sio = socketio_server

        super().__init__(socketio_server, other_asgi_app, socketio_path=socketio_path)  # type: ignore
