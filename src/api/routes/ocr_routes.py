from fastapi import APIRouter

from src.common.logger import Logger
from src.common.models import GenericResponse, create_response
from src.common.services.chatgpt import ChatGPTModel, ChatGPTService
from src.config import Config
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

    text_readed = data["text"]

    try:
        gpt_service = ChatGPTService(Config.OPENAI_KEY, ChatGPTModel.DAVINCI_TEXT_2)
        gpt = gpt_service.ask_receibe_data(text_readed)
    except Exception as e:
        print(e)
        Logger.error("Error with GPT")
        gpt = {}

    res = OCRResponse(text=data["text"], image=draw, gpt=gpt)

    return create_response(data=res, message="OCR applied successfully")
