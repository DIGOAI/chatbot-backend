import re

SERVICE_PHONE_PATTERN = r'(whatsapp:)(\+\d{12})'


def get_phone_and_service(text: str) -> tuple[str, str]:
    """Get the phone and service from a text

    Parameters:
    text (str): The text to parse

    Returns:
    tuple[str, str]: The phone and service
    """
    match = re.search(SERVICE_PHONE_PATTERN, text)

    if not match:
        raise ValueError("The text doesn't have a phone")

    return match.group(2), match.group(1)
