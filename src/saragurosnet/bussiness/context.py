from src.common.models import Client, Conversation
from src.common.models import TwilioWebHook as Event


class Context():
    """Context class to handle the context of the application."""

    def __init__(self, event: Event, client: Client | None, last_state: str | None, conversation: Conversation, waiting_for: str | None) -> None:
        self.event_twilio: Event = event
        self.client: Client | None = client
        self.conversation: Conversation = conversation
        self.last_state: str | None = last_state
        self.waiting_for: str | None = waiting_for

    def __str__(self) -> str:
        return f"Context(client={self.client}, conversation={self.conversation}, last_state={self.last_state}, waithing_for={self.waiting_for})"
