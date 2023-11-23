from fastapi import APIRouter

from src.common.cases import OCRUseCases
from src.common.models import GenericResponse, create_response
from src.ocr.types import OCRPayload, OCRResponse

router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.post("/", response_model=GenericResponse[OCRResponse])
def make_ocr(form: OCRPayload):
    res = OCRUseCases().extract_data_from_receibe(form.image)

    return create_response(data=res, message="OCR applied successfully")
