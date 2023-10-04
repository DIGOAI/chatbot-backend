import re
from typing import Optional

SERVICE_PHONE_PATTERN = r'^(whatsapp:)(\+\d{12})'
CI_RUC_PATTERN = r"^(0[1-9]|1\d|2[1-4])\d{8}(001)?$"


def get_phone_and_service(text: str) -> tuple[str, str]:
    """Get the phone and service from a text

    Parameters:
    text (str): The text to parse

    Returns:
    tuple[str, str]: The phone and service
    """
    match = re.search(SERVICE_PHONE_PATTERN, text)

    if not match:
        raise ValueError("The text doesn't match a phone")

    return match.group(2), match.group(1)


def get_ci_or_ruc(text: str) -> str:
    """Get the CI or RUC from a text

      Parameters:
      text (str): The text to parse

      Returns:
      str: The CI or RUC
      """
    matcher = re.compile(CI_RUC_PATTERN)

    match = matcher.search(text.strip())

    if not match:
        raise ValueError("The text doesn't match a CI or RUC")

    return match.string


def format_fullname(names: Optional[str], lastnames: Optional[str]):
    """Format the fullname

    Parameters:
    names (Optional[str]): The names of the user
    lastnames (Optional[str]): The lastnames of the user

    Returns:
    str: The fullname
    """
    names = names or ''
    lastnames = lastnames or ''
    return f"{names} {lastnames}".strip()
