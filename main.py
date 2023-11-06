# REST API
from src import api, chatbot

# socket.io
from src.socket import socketio_mount
from src.socket.routers import router as socketio_router_v1

app = api.create_app(
    title="ChatbotAPI | DIGO",
    version=api.__VERSION__,
    description=f"""Welcome to the **REST API** for the **Saragurosnet - Chatbot** service.
    \n\nPowered by `Digo-chatbot v{chatbot.__VERSION__}`""",
)

sio = socketio_mount(app)
socketio_router_v1(sio)

clients = []


@sio.on("connect", namespace="/chat")
def connect(sid, env):
    clients.append(sid)
    print("--> clients: ", clients)


@sio.on("disconnect", namespace="/chat")
def disconnect(sid):
    clients.remove(sid)
    print("--> clients: ", clients)


@sio.on("messages")
async def messages(sid, data):
    await sio.emit("response", "I'm the server")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore
