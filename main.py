from src import api, chatbot

app = api.create_app(
    title="ChatbotAPI | DIGO",
    version=api.__VERSION__,
    description=f"""Welcome to the **REST API** for the **Saragurosnet - Chatbot** service.
    \n\nPowered by `Digo-chatbot v{chatbot.__VERSION__}`""",
)
