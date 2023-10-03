from src import create_app
from src.version import __VERSION__

app = create_app(
    title="ChatbotAPI | DIGO",
    version=__VERSION__,
    description="This is the API for the Chatbot project.",
)
