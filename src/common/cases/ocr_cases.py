from src.common.cases.base_use_cases import UseCaseBase
from src.common.logger import Logger
from src.common.services.chatgpt import ChatGPTModel, ChatGPTService
from src.config import Config
from src.ocr import apply_ocr
from src.ocr.types import OCRResponse

_gpt_service = ChatGPTService(Config.OPENAI_KEY, ChatGPTModel.DAVINCI_TEXT_2)


class OCRUseCases(UseCaseBase):

    def extract_data_from_receibe(self, image: str):
        data, draw = apply_ocr(image,
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

        return OCRResponse(text=data["text"], image=draw, gpt=gpt)
