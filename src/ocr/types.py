from typing import Any, Optional, TypedDict

from pydantic import BaseModel, Field


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
    text: str = Field(examples=["A text result from the OCR"])
    image: Optional[str] = Field(examples=["A base64 image"])
    gpt: dict[str, Any]
