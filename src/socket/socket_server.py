from typing import TYPE_CHECKING

from socketio import ASGIApp  # type: ignore

from src.utils.singleton import Singleton

if TYPE_CHECKING:
    from fastapi import FastAPI
    from socketio import AsyncServer  # type: ignore


class FastAPIWithSIO(ASGIApp):

    def __init__(self,  socketio_server: "AsyncServer", other_asgi_app: "FastAPI", socketio_path: str = 'socket.io'):
        super().__init__(socketio_server, other_asgi_app, socketio_path=socketio_path)  # type: ignore
        SocketServer.Instance().set_socket(socketio_server)


@Singleton
class SocketServer:
    def __init__(self):
        self.socket: "AsyncServer"

    def set_socket(self, socket_server: "AsyncServer"):
        self.socket = socket_server
