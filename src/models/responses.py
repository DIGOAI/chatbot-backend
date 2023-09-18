from typing import Generic, Literal, Optional, TypeVar

from fastapi import status as STATUS
from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class GenericResponse(BaseModel, Generic[T]):
    message: str
    status: Literal["ok"] | Literal["error"]
    data: T
    error: Optional[str] = None


def create_response(data: T,  # type: ignore
                    message: str = "Success",
                    status_code: int = STATUS.HTTP_200_OK,
                    status: Literal["ok"] | Literal["error"] = "ok", error: str | None = None) -> JSONResponse:
    """Return a success response

    Parameters:
    data (T): The data of the response
    message (str): The message of the response
    status_code (int): The status code of the response
    status (str): The status of the response
    """

    return JSONResponse(
        status_code=status_code,
        content=GenericResponse[T](message=message, status=status, data=data).model_dump(),
    )
