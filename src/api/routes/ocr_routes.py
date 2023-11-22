import json

from fastapi import APIRouter

from src.common.models import GenericResponse, create_response
from src.ocr import apply_ocr
from src.ocr.types import OCRPayload, OCRResponse

router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.post("/", response_model=GenericResponse[OCRResponse])
def make_ocr(form: OCRPayload):
    data, draw = apply_ocr(form.image,
                           remove_bg=True,
                           draw_boxes_on_image=True,
                           contrast=1.45,
                           brightness=1.1,
                           sharpness=3,
                           smooth=False,
                           smooth_factor=1,
                           apply_grayscale=True,
                           confidence_threshold=-1000, to_base64=True)
    res = OCRResponse(text=data["text"], image=draw)

    return create_response(data=res, message="OCR applied successfully")
