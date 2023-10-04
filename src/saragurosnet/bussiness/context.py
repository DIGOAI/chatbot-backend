from src.common.models import Client
from src.common.models import TwilioWebHook as Event


class Context():
    """Context class to handle the context of the application."""

    def __init__(self, event: Event, client: Client) -> None:
        self.event_twilio: Event = event
        self.client: Client = client
