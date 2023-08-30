from typing import Optional

from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance


class TwilioService(object):
    """Class to manage the connection to the Twilio API.

    Parameters:
    account_sid (str): The account sid
    auth_token (str): The auth token
    sender (str): The sender phone number
    receiver (str): The receiver phone number
    """

    def __init__(self, account_sid: str, auth_token: str, sender: str, receiver: str) -> None:
        self._client = Client(account_sid, auth_token)
        self._sender = sender
        self._receiver = receiver

    def __call__(self, msg: str, sender: Optional[str] = None, receiver: Optional[str] = None) -> MessageInstance:
        """Send a message.

        Parameters:
        msg (str): The message to send
        sender (str): The sender phone number
        receiver (str): The receiver phone number
        """
        return self._client.messages.create(
            body=msg,
            from_=sender or self._sender,
            to=receiver or self._receiver
        )
