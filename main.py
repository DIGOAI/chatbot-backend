from src import api

app = api.create_app(
    title="ChatbotAPI | DIGO",
    version=api.__VERSION__,
    description="This is the API for the Saragurosnet Chatbot",
)
