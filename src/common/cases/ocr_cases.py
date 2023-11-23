from src.common.cases.base_use_cases import UseCaseBase
from src.ocr import apply_ocr


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

        return data["text"], draw
