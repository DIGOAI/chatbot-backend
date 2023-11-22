import json
from enum import Enum
from typing import Any, TypedDict, cast

import openai

from src.common.services.chatgpt.promps import OCR_DATA_PROMPT, TICKET_TYPE_PROMPT
from src.config import Config

openai.api_key = Config.OPENAI_KEY


class ChoiceType(TypedDict):
    text: str
    index: int


class ChatGPTResponseType(TypedDict):
    choices: list[ChoiceType]


class ChatGPTModel(str, Enum):
    """The models available for ChatGPT.

    Attributes:
    DAVINCI_CODE (str): The base model for code completion tasks.
    DAVINCI_TEXT_1 (str): The InstructGPT model based on code-davinci-002.
    DAVINCI_TEXT_2 (str): An improvement on text-davinci-002.
    DAVINCI_TURBO (str): An improvement on text-davinci-003, optimized for chat.
    """

    DAVINCI_CODE = "code-davinci-002"
    DAVINCI_TEXT_1 = "text-davinci-002"
    DAVINCI_TEXT_2 = "text-davinci-003"
    DAVINCI_TURBO = "gpt-3.5-turbo-0301"


class ChatGPTService(object):
    """The ChatGPT service class to interact with OpenAI API."""

    def __init__(self, api_key: str, model: ChatGPTModel = ChatGPTModel.DAVINCI_TEXT_2, temperature: float = 0.5, max_tokens: int = 1024) -> None:
        openai.api_key = api_key
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    def _make_completion(self, prompt: str, **kwargs: dict[str, Any]):
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

    def ask_ticket_type(self, msg: str) -> tuple[str, str]:
        """Ask ChatGPT for the category of the message.

        ChatGPT is requested to determine, based on a message sent by the user, 
        which category the message most likely belongs to, within a list of 
        categories contained in the prompt.

        Parameters:
        msg (str): The message sent by the user.

        Returns:
        tuple[str, str]: The subject category and department suggested by ChatGPT.
        """

        prompt = TICKET_TYPE_PROMPT.format(message=msg)

        completion = self._make_completion(prompt=prompt)  # type: ignore

        # TODO: Review this casts. Review the replacement of the regex.
        res = completion["choices"][0]['text'].replace(r'[\s\.\n]', '')

        # TODO: Review this split.
        subject, department = res.split(", ")

        return subject, department

    def ask_receibe_data(self, text_data: str) -> dict[str, Any]:
        """Ask ChatGPT for the data extracted from a receipt.

        ChatGPT is requested to determine, based on the text of a receipt, the 
        data contained in it.

        Parameters:
        text_data (str): The text of the receipt.

        Returns:
        dict[str, Any]: The data extracted from the receipt.
        """

        prompt = OCR_DATA_PROMPT.format(text_data=text_data)

        completion = self._make_completion(prompt=prompt)

        response = completion["choices"][0]["text"]

        res_dict = json.loads(response)

        return res_dict
