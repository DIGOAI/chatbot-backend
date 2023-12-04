from typing import Literal, overload

import pytesseract  # type: ignore
from PIL import Image
from pytesseract import Output  # type: ignore

from src.ocr.background import remove_bg_image
from src.ocr.images import (
    base64_to_image,
    download_image_from_url,
    draw_boxes,
    has_white_background,
    image_to_base64,
    preprocess,
)
from src.ocr.types import OCRData, TesseractData, TextNotExtractedException


@overload
def apply_ocr(
    image: Image.Image | str,
    remove_bg: bool = True,
    auto_remove_bg: bool = True,
    draw_boxes_on_image: bool = False,
    contrast: float = 1.5,
    brightness: float = 1.0,
    smooth: bool = True,
    smooth_factor: int = 3,
    apply_grayscale: bool = True,
    sharpness: float = 1.0,
    confidence_threshold: int = 40,
    to_base64: Literal[False] = False
) -> tuple[OCRData, Image.Image | None]:
    ...


@overload
def apply_ocr(
    image: Image.Image | str,
    remove_bg: bool = True,
    auto_remove_bg: bool = True,
    draw_boxes_on_image: bool = False,
    contrast: float = 1.5,
    brightness: float = 1.0,
    smooth: bool = True,
    smooth_factor: int = 3,
    apply_grayscale: bool = True,
    sharpness: float = 1.0,
    confidence_threshold: int = 40,
    to_base64: Literal[True] = True
) -> tuple[OCRData, str | None]:
    ...


def apply_ocr(
    image: Image.Image | str,
    remove_bg: bool = True,
    auto_remove_bg: bool = True,
    draw_boxes_on_image: bool = False,
    contrast: float = 1.5,
    brightness: float = 1.0,
    smooth: bool = True,
    smooth_factor: int = 3,
    apply_grayscale: bool = True,
    sharpness: float = 1.0,
    confidence_threshold: int = 40,
    to_base64: bool = False
):

    if isinstance(image, str):
        if image.startswith("http"):
            image = download_image_from_url(image)
        else:
            image = base64_to_image(image)

    has_white_bg = has_white_background(image, tolerance=50, white_pixel_percentage_threshold=70)

    if remove_bg or (auto_remove_bg and not has_white_bg):
        image = remove_bg_image(image)

    image = preprocess(image, apply_grayscale, contrast, brightness, smooth, smooth_factor,  sharpness)

    data: TesseractData = pytesseract.image_to_data(image, output_type=Output.DICT)  # type: ignore
    draw: Image.Image | str | None = None

    if draw_boxes_on_image:
        draw = draw_boxes(image, data, confidence_threshold=confidence_threshold)  # type: ignore

        if to_base64:
            draw = image_to_base64(draw)

    text = [t.strip() for t in data.get("text") if t.strip() != ""]

    if not text:
        raise TextNotExtractedException()

    new_data: OCRData = {
        "text": ", ".join(text)
    }

    return new_data, draw
