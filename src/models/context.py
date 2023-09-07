from typing import TypedDict

from src.models.event import Event
from src.services.chat_api import ChatApiService
from src.services.saragurosnet import SaragurosService
from src.services.twilio import TwilioService


# TODO: Review with Aminael if this value types are correct
class ContextType(TypedDict):
    """ContextType class to handle the context of the application."""

    EVENT_TWILIO: Event
    DATA_USER_ID: int
    DATA_USER_CI: str | None
    DATA_LAST_STATUS: str
    SERVICE_API: ChatApiService
    SERVICE_SARAGUROS: SaragurosService
    SERVICE_TWILIO: TwilioService
