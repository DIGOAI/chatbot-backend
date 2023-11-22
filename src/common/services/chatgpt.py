from enum import Enum
from typing import Any, cast

import openai

from src.config import Config

openai.api_key = Config.OPENAI_KEY

PROMPT = """El siguiente es un mensaje de un cliente en un canal de sorpote:

{message}.

A partir del mensaje del cliente determina a cuál de las siguientes categorías de atención pertenece el mensaje:

- Disponibilidad del servicio por falla técnica.
- Lentitud o baja velocidad del servicio.
- Problemas con la antena o baja señal de equipo CPE.
- Problemas del servicio por ausencia o falla en potencia óptica.
- Problemas con el router o señal WIFI.
- Cambio de clave WIFI.
- Bloqueo de servicios o accesos a internet.
- Falla masiva.
- Congelamiento temporal del servicio.
- Traslado del servicio.
- Cambio de condiciones del servicio.
- Suspensión Injustificada.
- Cesión de contrato.
- Servicios adicionales.
- Contratación de servicios.
- Equipos en comodato.
- Terminación de contrato.
- Certificaciones y paz y salvo.
- Fidelización.
- Reclamo sobre reporte a centrales de riesgos.
- Cambio de periodos de facturación.
- Reclamo sobre facturación.
- Descuento o compensación.
- Recurso de reposición.
- Recurso de reposición y en subsidio de apelación.
- Cumplimiento de una orden de la SIC.
- Sugerencias.
- Otras PQ.

Selecciona además qué departamento debería atender al usuario:

- Soporte técnico
- Ventas
- Quejas y Sugerencias.

El output debe ser estrictamente: "categoría sugerida, departamento sugerido"
"""


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

    def _make_completion(self, prompt: str, **kwargs: dict[str, Any]):  # type: ignore
        """Make a completion request to OpenAI API.

        Parameters:
        prompt (str): The prompt to send to OpenAI API.
        **kwargs: The other arguments to send to OpenAI API.

        Returns:
        dict: The response from OpenAI API.
        """
        return openai.Completion.create(  # type: ignore
            engine=self._model,
            prompt=prompt,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            **kwargs
        )

    def ask_chatgpt(self, msg: str) -> tuple[str, str]:
        """Ask ChatGPT for the category of the message.

        ChatGPT is requested to determine, based on a message sent by the user, 
        which category the message most likely belongs to, within a list of 
        categories contained in the prompt.

        Parameters:
        msg (str): The message sent by the user.

        Returns:
        tuple[str, str]: The subject category and department suggested by ChatGPT.
        """

        prompt = PROMPT.format(message=msg)

        completion = self._make_completion(prompt=prompt)  # type: ignore

        # TODO: Review this casts. Review the replacement of the regex.
        res = cast(str, cast(dict[str, Any], completion)[
                   "choices"][0]['text']).replace(r'[\s\.\n]', '')

        # TODO: Review this split.
        subject, department = res.split(", ")

        return subject, department


def fix_chatgpt_response(text: str):
    """Corrects the end of sentences with a final point."""
    split = text.split(".")[:-1]
    result = ".".join(split) + "."
    return result


def ask_to_chatgpt_v1(prompt: str,
                      engine: str = "text-davinci-003",
                      max_tokens: int = 500,
                      fixed: bool = False):
    """Talk with chatGPT."""
    completion = openai.Completion.create(engine=engine,
                                          prompt=prompt,
                                          max_tokens=max_tokens)
    response = completion.choices[0].text
    if fixed:
        response = fix_chatgpt_response(response)
    return response


def ask_to_chatgpt_v2(prompt: str,
                      model: str = "gpt-3.5-turbo",
                      max_tokens: int = 500,
                      fixed: bool = False,
                      history: list = None):
    """Talk with chatGPT."""
    current_message = [{"role": "user", "content": prompt}]
    if history is not None and isinstance(history, list):
        history.extend(current_message)
        messages = history
    else:
        messages = current_message
    completion = openai.ChatCompletion.create(model=model,
                                              messages=messages,
                                              max_tokens=max_tokens,
                                              stream=False)
    response = completion.choices[0].message["content"]
    if fixed:
        response = fix_chatgpt_response(response)
    return response


def ask_to_chatgpt(prompt: str,
                   model: str = "gpt-3.5-turbo",
                   engine: str = "text-davinci-003",
                   max_tokens: int = 500,
                   fixed: bool = False,
                   history: list = None,
                   api_version: int = 1
                   ):
    """ask to chatgpt."""
    if api_version == 1:
        response = ask_to_chatgpt_v1(
            prompt=prompt,
            engine=engine,
            max_tokens=max_tokens,
            fixed=fixed
        )
        return response

    if api_version == 2:
        response = ask_to_chatgpt_v2(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            history=history,
            fixed=fixed
        )
        return response
