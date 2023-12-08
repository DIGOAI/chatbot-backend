from src import api, chatbot, socket
from src.socket import FastAPIWithSIO

api_app = api.create_app(
    title="ChatbotAPI | DIGO",
    version=api.__VERSION__,
    description=f"""Welcome to the **REST API** for the **Saragurosnet - Chatbot** service.
    \n\nPowered by `Digo-chatbot v{chatbot.__VERSION__}`""",
)

sio_app = socket.create_socket()

app = FastAPIWithSIO(sio_app, api_app, 'socket.io')


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore
