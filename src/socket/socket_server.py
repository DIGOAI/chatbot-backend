from typing import Self

from fastapi import FastAPI
from socketio import ASGIApp, AsyncServer  # type: ignore


class FastAPIWithSIO(ASGIApp):

    def __init__(self,  socketio_server: AsyncServer, other_asgi_app: FastAPI | None = None, socketio_path: str = 'socket.io'):
        super().__init__(socketio_server, other_asgi_app, socketio_path=socketio_path)  # type: ignore

    def get_sio(self) -> AsyncServer:
        return self.engineio_server


class SocketServer:
    _instance: Self | None = None
    _socket_server: FastAPIWithSIO

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @classmethod
    def socket(cls):
        return cls._socket_server.get_sio()

    @classmethod
    def set_socket_server(cls, socket_server: FastAPIWithSIO):
        cls._socket_server = socket_server
