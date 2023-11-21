import base64
import os
import re
from io import BytesIO
from typing import List, Literal, Union

import numpy as np
import pytesseract
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from pytesseract import Output


def draw_boxes(image: Image.Image, data: dict, confidence_threshold: int = 80):
    image = image.convert("RGB")
    n_boxes = len(data["text"])
    draw = ImageDraw.Draw(image)

    for i in range(n_boxes):
        text = data["text"][i]
        if len(text) < 1:
            continue
        conf = int(data["conf"][i])
        if conf > confidence_threshold:
            (x, y, w, h) = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
            draw.rectangle([x, y, x + w, y + h], outline=(0, 255, 0), width=2)
    return image


def grayscale(image: Image.Image):
    return image.convert("L")


def remove_noise(image: Image.Image, filter_size: int = 3):
    return image.filter(ImageFilter.MedianFilter(size=filter_size))


def adjust_contrast(image: Image.Image, factor: float = 1.1):
    enhancer = ImageEnhance.Contrast(image)
    image_with_adjusted_contrast = enhancer.enhance(factor)
    return image_with_adjusted_contrast


def adjust_brightness(image: Image.Image, factor: float = 1):
    enhancer = ImageEnhance.Brightness(image)
    result = enhancer.enhance(factor)
    return result


def adjust_contrast(image: Image.Image, factor: float = 1.1):
    enhancer = ImageEnhance.Contrast(image)
    result = enhancer.enhance(factor)
    return result


def adjust_brightness(image: Image.Image, factor: float = 1):
    enhancer = ImageEnhance.Brightness(image)
    result = enhancer.enhance(factor)
    return result


def adjust_sharpness(image: Image.Image, factor: float = 1):
    enhancer = ImageEnhance.Sharpness(image)
    result = enhancer.enhance(factor)
    return result


def preprocess(image: Image.Image, apply_grayscale: bool = True, contrast: float = 1.5, brightness: float = 1, smooth: bool = True, smooth_factor: float = 1, sharpness: float = 1.0):
    if apply_grayscale:
        image = grayscale(image)
    image = adjust_contrast(image, contrast)
    image = adjust_brightness(image, brightness)
    image = adjust_sharpness(image, sharpness)
    if smooth:
        image = remove_noise(image, smooth_factor)
    return image


def thresholding(image: Image.Image, min_: int = 100, max_: int = 255):
    return image.point(lambda p: p > min_ and max_)


def dilate(image: Image.Image):
    kernel = ImageFilter.Kernel((3, 3), [1, 1, 1, 1, 1, 1, 1, 1, 1])
    return image.filter(ImageFilter.MinFilter(size=3))


def erode(image: Image.Image):
    kernel = ImageFilter.Kernel((3, 3), [1, 1, 1, 1, 1, 1, 1, 1, 1])
    return image.filter(ImageFilter.MaxFilter(size=3))


def opening(image: Image.Image):
    kernel = ImageFilter.Kernel((3, 3), [1, 1, 1, 1, 1, 1, 1, 1, 1])
    return image.filter(ImageFilter.MinFilter(size=3)).filter(ImageFilter.MaxFilter(size=3))


def canny(image: Image.Image):
    return image.filter(ImageFilter.FIND_EDGES)


def deskew(image: Image.Image):
    return image.rotate(-image.getexif().get(274, 0))


def match_template(image: Image.Image, template):
    result = image.filter(ImageFilter.FIND_EDGES). \
        filter(ImageFilter.MinFilter(size=3)). \
        filter(ImageFilter.MaxFilter(size=3)). \
        filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    return result


def base64_to_image(base64_string: str) -> Image.Image:
    """Returns a PIL image as a base64 encoded string."""

    if ";base64," in base64_string:
        split = base64_string.split(";base64")
        # mime_type = split[0]
        base64_string = split[1]

    image_bytes = base64.b64decode(base64_string)
    buffer = BytesIO(image_bytes)
    image = Image.open(buffer)
    return image


def image_to_base64(
    image: Union[str, Image.Image, np.ndarray],
    _format: str = "jpeg",
    myme: bool = True,
) -> str:
    """Returns a base64 string from a PIL Image."""
    if isinstance(image, str):
        return image

    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffer = BytesIO()
    image.save(buffer, format=_format)
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    if myme:
        myme_type = f"data:image/{_format};base64,"
        encoded_image = f"{myme_type}{encoded_image}"

    return encoded_image


def parse_image(image: Union[str, Image.Image, np.ndarray]):
    """Returns an image as PIL image"""
    if isinstance(image, str):
        image = base64_to_image(image)

    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    return image


def parse_list_of_images(images: List) -> List[Image.Image]:
    """Converts a list of images as PIL image"""
    results = [parse_image(image) for image in images]
    return results


def save_list_of_images(images: List, filepath: str, prefix: str = None):
    """Save list of images."""
    for index, image in enumerate(images):
        prefix = f"{prefix}_" if prefix is not None else ""
        name = f"{prefix}{index}.jpeg"
        fullfilepath = os.path.join(filepath, name)
        image = parse_image(image)
        image.save(fullfilepath)


def download_image_from_url(url: str):
    """Return an image object given a url."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    content = response.content
    image = Image.open(BytesIO(content))
    return image


def download_images_from_array_of_urls(urls: List[str]):
    """Given an array of urls returns an array of downloaded images."""
    images = []
    for url in urls:
        image = download_image_from_url(url)
        images.append(image)
    return images


def has_white_background(image: Image.Image, tolerance: int = 10, white_pixel_percentage_threshold: int = 80) -> bool:
    """Checks if an image has a white background.
    Args:
        image: a Pillow image.
        tolerance: min value to consider a pixel as white (0 - 255)
        white_pixel_percentage_threshold (0 - 100)
    """
    image = image.convert("L")
    image = image.filter(ImageFilter.GaussianBlur(radius=11))
    img_array = np.array(image)
    threshold = 255 - tolerance
    # white_pixels = (img_array[:, :, 0] > threshold) & (
    #     img_array[:, :, 1] > threshold) & (img_array[:, :, 2] > threshold)
    white_pixels = (img_array > threshold)
    white_pixel_percentage = (np.sum(white_pixels) / img_array.size) * 100
    # print("white percentage: ", white_pixel_percentage, img_array.min(),
    #       img_array.max(), img_array.mean(), np.median(img_array))
    return white_pixel_percentage >= white_pixel_percentage_threshold
