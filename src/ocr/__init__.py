from typing import Any, Union

import pytesseract
from PIL import Image
from pytesseract import Output

from src.ocr.background import remove_bg_image
from src.ocr.images import (
    base64_to_image,
    download_image_from_url,
    draw_boxes,
    has_white_background,
    image_to_base64,
    preprocess,
)


def _get_text_from_image(image: Image.Image):
    return pytesseract.image_to_string(image)


def _get_data_from_image(image: Image.Image):
    return pytesseract.image_to_data(image, output_type=Output.DICT)


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
) -> tuple[dict[str, Any], Image.Image | str | None]:

    if not isinstance(image, Image.Image | str):
        raise ValueError("`image` type is not valid!")

    if isinstance(image, str):
        if image.startswith("http"):
            image = download_image_from_url(image)
        else:
            image = base64_to_image(image)

    has_white_bg = has_white_background(image, tolerance=50, white_pixel_percentage_threshold=70)

    if remove_bg:
        if auto_remove_bg and not has_white_bg:
            image = remove_bg_image(image)

        if not auto_remove_bg:
            image = remove_bg_image(image)

    image = preprocess(
        image,
        contrast=contrast,
        brightness=brightness,
        smooth=smooth,
        smooth_factor=smooth_factor,
        apply_grayscale=apply_grayscale,
        sharpness=sharpness
    )

    data = _get_data_from_image(image)

    draw = None

    if draw_boxes_on_image:
        draw = draw_boxes(image, data, confidence_threshold=confidence_threshold)
        if to_base64:
            draw = image_to_base64(draw)
    data["string"] = " ".join(data.get('text'))
    return data, draw
