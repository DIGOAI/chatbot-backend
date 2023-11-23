import json
from typing import Any

from src.common.cases.base_use_cases import UseCaseBase
from src.common.services import chatgpt
from src.common.services.chatgpt import promps
from src.common.services.chatgpt.types import InsuficientDataError, ReceibeData
from src.config import Config

_gpt_service = chatgpt.ChatGPTService(Config.OPENAI_KEY, chatgpt.ChatGPTModel.DAVINCI_TEXT_2)


class ChatGPTUseCases(UseCaseBase):

    def ask_receibe_data(self, text_data: str):
        """Ask ChatGPT for the data extracted from a receipt.

        ChatGPT is requested to determine, based on the text of a receipt, the 
        data contained in it.

        Parameters:
        text_data (str): The text of the receipt.

        Returns:
        dict[str, Any]: The data extracted from the receipt.
        """

        prompt = promps.OCR_DATA_PROMPT.format(text_data=text_data)
        completion = _gpt_service.ask_chatGPT(prompt=prompt)

        response = completion["choices"][0]["text"]

        try:
            data: dict[str, Any] = json.loads(response)
            return ReceibeData(**data)
        except Exception:
            raise InsuficientDataError(data=response)

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

        prompt = promps.TICKET_TYPE_PROMPT.format(message=msg)
        completion = _gpt_service.ask_chatGPT(prompt=prompt)  # type: ignore

        # TODO: Review this casts. Review the replacement of the regex.
        res = completion["choices"][0]['text'].replace(r'[\s\.\n]', '')

        # TODO: Review this split.
        subject, department = res.split(", ")

        return subject, department
