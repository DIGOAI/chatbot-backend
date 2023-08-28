import json
import re
from typing import Any, cast

import requests

from src.config import Config
from src.models import Receipt


class OCRLambdaService(object):
    """Class to manage the OCR Lambda service."""

    def __init__(self):
        self.base_url = Config.OCR_LAMBDA_URL
        self.headers = {"Content-Type": "application/json"}

    def _make_request(self, data: dict[str, Any]) -> dict[str, Any]:
        """Make a request to the OCR Lambda service.

        Parameters:
        data (dict[str, Any]): The data to send in the request

        Returns:
        dict[str, Any]: The result of the request
        """

        response = requests.post(
            self.base_url, headers=self.headers, data=json.dumps(data))

        return response.json()

    def _ocr(self, image: str) -> dict[str, Any]:
        """Get the text from an image.

        Parameters:
        image (str): The image url to get the text

        Returns:
        dict[str, Any]: The result of the request
        """
        data = {"image_url": image}

        return self._make_request(data)

    def parse_transaction(self, receipt_url: str) -> Receipt:
        """Parse a receipt from a bank transfer.

        Parameters:
        receipt_url (str): The receipt url to parse

        Returns:
        Receipt: The parsed receipt

        Raises:
        ValueError: If the receipt is invalid
        """
        res = self._ocr(receipt_url)

        lines = cast(str, res["image_text"]).split("\n")

        match = re.search(r'COAC.*JARDIN AZUAYO', lines[0])

        if not match:
            raise ValueError("Invalid receipt")

        return Receipt(
            user_name=lines[4],
            date=lines[7],
            amount=lines[15],
            office=lines[16]
        )
