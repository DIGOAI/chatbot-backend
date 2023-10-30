# REST API
from src import api, chatbot

# socket.io
from src.socket import socketio_mount

app = api.create_app(
    title="ChatbotAPI | DIGO",
    version=api.__VERSION__,
    description=f"""Welcome to the **REST API** for the **Saragurosnet - Chatbot** service.
    \n\nPowered by `Digo-chatbot v{chatbot.__VERSION__}`""",
)

sio = socketio_mount(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore
