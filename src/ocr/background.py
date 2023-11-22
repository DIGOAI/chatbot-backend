from typing import Literal, cast, overload

from PIL import Image
from rembg import remove  # type: ignore

from src.ocr.images import image_to_base64


@overload
def remove_bg_image(image: Image.Image, to_base64: Literal[False] = False, myme: bool = True, _format: str = "jpeg") -> Image.Image:
    ...


@overload
def remove_bg_image(image: Image.Image, to_base64: Literal[True] = True, myme: bool = True, _format: str = "jpeg") -> str:
    ...


def remove_bg_image(image: Image.Image, to_base64: bool = False, myme: bool = True, _format: str = "jpeg") -> str | Image.Image:
    """Removes the background from an image using rembg.

    Attributes:
    image (Image.Image): The image to remove the background from.
    to_base64 (bool, optional): Whether to return the result as a base64 string. Defaults to False.
    myme (bool, optional): Whether to return the result as a myme string. Defaults to True.
    _format (str, optional): The format of the image. Defaults to "jpeg".

    Raises:
    ValueError: If the result is not a PIL Image.

    Returns:
    str | Image.Image: The result as a base64 string or PIL Image.
    """

    result = cast(Image.Image, remove(image))

    if to_base64:
        if not isinstance(result, Image.Image):  # type: ignore
            raise ValueError("Result should be a PIL Image")

        result = image_to_base64(result, _format=_format, myme=myme)

    return result
