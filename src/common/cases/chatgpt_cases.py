from src.common.cases.base_use_cases import UseCaseBase
from src.common.services.chatgpt import ChatGPTModel, ChatGPTService
from src.config import Config

_gpt_service = ChatGPTService(Config.OPENAI_KEY, ChatGPTModel.DAVINCI_TEXT_2)


class ChatGPTUseCases(UseCaseBase):

    def ask_receibe_data(self, text: str):
        return _gpt_service.ask_receibe_data(text)
