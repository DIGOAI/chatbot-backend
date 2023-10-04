from typing import Any, Literal, Optional, Type, TypeVar

import requests
from pydantic import BaseModel

from src.common.logger import Logger

T = TypeVar('T', bound=BaseModel)

MethodRequest = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]


class Requester:
    """Requester class to handle the requests to any API.

    Parameters:
    url (str): The url of the API
    token (Optional[str]): The token to authenticate the requests
    """

    def __init__(self, base_url: str, token: Optional[str] = None):
        self._base_url = base_url
        self._token = token
        self._headers = {"Content-Type": "application/json"}

        if self._token:
            # self._headers["Authorization"] = f"Bearer {self._token}"
            self._headers["X-API-KEY"] = self._token

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[Any]):
        if exc_type is not None:
            Logger.error(f"{exc_type.__name__}: {exc_value}")

    def make_request(self, method: MethodRequest, endpoint: str, data: Optional[dict[str, Any]] = None, response_model: Optional[Type[T]] = None) -> Optional[T] | None:
        """Make a request to the API.

        Parameters:
        method (MethodRequest): The method of the request (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`, `HEAD`)
        endpoint (str): The endpoint of the request
        data (Optional[dict[str, Any]]): The data of the request
        response_model (Optional[Type[T]]): The model of the response

        Returns:
        Optional[T] | Any: The result of the request
        """

        full_url = f"{self._base_url}{endpoint}" if endpoint.startswith("/") else f"{self._base_url}/{endpoint}"
        response = requests.request(method, full_url, headers=self._headers, json=data)

        if response.status_code == 200:
            if response_model:
                return response_model.model_validate(response.json())
            else:
                return response.json()  # Si no se proporciona un modelo, devolver el texto sin procesar
        else:
            response.raise_for_status()
