import json

from fastapi import APIRouter

from src.common.models.ocr import MakeOCRForm, MakeOCRResponse
from src.common.services.chatgpt import ask_to_chatgpt
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
    string = data.get("string")
    prompt = f"""
        Extract data from the following text obtained from a receipt:

        {string}

        Return a JSON as Follows:
        `{{
            "bank": "bank from text, put null if not found",
            "customer": "name of the customer from" or null,
            "date": "date from text on format dd/MM/yyyy" or null,
            "hour": "hour from text on format HH:mm" or null,
            "currency": "currency from text" or null,
            "total": <numeric value> or null
        }}`
    """

    try:
        gpt = ask_to_chatgpt(prompt, api_version=2)
        gpt = json.loads(gpt)
    except:
        gpt = {}

    response = {
        "gpt": gpt,
        "text": string,
        "image": draw
    }
    return response
