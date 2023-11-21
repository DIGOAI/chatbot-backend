from fastapi import APIRouter

from src.common.models.ocr import MakeOCRForm, MakeOCRResponse
from src.ocr import apply_ocr

#
router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.post("/", response_model=MakeOCRResponse)
def make_ocr(form: MakeOCRForm):
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
    response = {
        "text": data.get("string"),
        "image": draw
    }
    return response
