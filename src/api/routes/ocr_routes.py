from fastapi import APIRouter

from src.common.cases import ChatGPTUseCases, OCRUseCases
from src.common.models import GenericResponse, create_response
from src.ocr.types import OCRPayload, OCRResponse

router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.post("/", response_model=GenericResponse[OCRResponse])
def make_ocr(form: OCRPayload):
    text, draw = OCRUseCases().extract_data_from_receibe(form.image)
    data_extracted = ChatGPTUseCases().ask_receibe_data(text)

    return create_response(data=OCRResponse(text=text, image=draw, gpt=data_extracted), message="OCR applied successfully")
