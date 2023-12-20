from enum import Enum
from typing import Any, TypedDict, cast

import openai

from src.config import Config

openai.api_key = Config.OPENAI_KEY


class ChoiceType(TypedDict):
    text: str
    index: int


class ChatGPTResponseType(TypedDict):
    choices: list[ChoiceType]


class ChatGPTModel(str, Enum):
    """The models available for ChatGPT.

    DEPRECATED models at 2024, see https://platform.openai.com/docs/deprecations

    Attributes:
    DAVINCI_CODE (str): The base model for code completion tasks.
    DAVINCI_TEXT_1 (str): The InstructGPT model based on code-davinci-002.
    DAVINCI_TEXT_2 (str): An improvement on text-davinci-002.
    DAVINCI_TURBO (str): An improvement on text-davinci-003, optimized for chat.
    """

    DAVINCI_CODE = "code-davinci-002"  # DEPRECATED at 2023-03-23 | Chat model replace with gpt-4
    DAVINCI_TEXT_1 = "text-davinci-002"  # DEPRECATED at 2024-01-04 | Chat model replace with gpt-3.5-turbo-instruct
    DAVINCI_TEXT_2 = "text-davinci-003"  # DEPRECATED at 2024-01-04 | Chat model replace with gpt-3.5-turbo-instruct
    DAVINCI_TURBO = "gpt-3.5-turbo-0301"  # DEPRECATED at 2024-06-13 | Chat model replace with gpt-3.5-turbo-0613


class ChatGPTService(object):
    """The ChatGPT service class to interact with OpenAI API."""

    def __init__(self, api_key: str, model: ChatGPTModel = ChatGPTModel.DAVINCI_TEXT_2, temperature: float = 0.5, max_tokens: int = 1024) -> None:
        openai.api_key = api_key
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    def ask_chatGPT(self, prompt: str, **kwargs: dict[str, Any]):
        """Make a completion request to OpenAI API.

        Parameters:
        prompt (str): The prompt to send to OpenAI API.
        **kwargs: The other arguments to send to OpenAI API.

        Returns:
        dict: The response from OpenAI API.
        """
        return cast(ChatGPTResponseType, openai.Completion.create(  # type: ignore
            engine=self._model,
            prompt=prompt,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            **kwargs
        ))
