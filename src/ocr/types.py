from typing import Optional, TypedDict

from pydantic import BaseModel, Field

from src.common.services.chatgpt.types import ReceibeData


class TesseractData(TypedDict):
    text: list[str]
    left: list[float]
    top: list[float]
    width: list[float]
    height: list[float]
    conf: list[float]


class OCRData(TypedDict):
    text: str


class OCRPayload(BaseModel):
    image: str = Field(
        examples=["Some base64 image, or some image url `https://pbs.twimg.com/media/D8zt8pcWwAQeRZI.jpg`"])


class OCRResponse(BaseModel):
    extracted_text: str = Field(examples=["A text result from the OCR"])
    extracted_data: ReceibeData
    image_with_boxes: Optional[str] = Field(examples=["A base64 image"])


class TextNotExtractedException(Exception):
    """The exception raised when the text cannot be extracted from the image."""

    message: str = "The text could not be extracted from the image."

    def __init__(self) -> None:
        super().__init__(self.message)
