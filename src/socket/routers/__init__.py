from socketio import ASGIApp

from src.socket.routers.chat import router as router_chat


def router(sio: ASGIApp):
    router_chat(sio)
