from enum import StrEnum


class SIOEvent(StrEnum):
    """SocketIO events"""

    CLIENT_SEND_MESSAGE = "FRONTEND_SEND_MESSAGE_EVENT"
    SERVER_NOTIFY_FRONTEND = "SERVER_NOTIFY_FRONTEND_NEW_MESSAGE_EVENT"


__all__ = ["SIOEvent"]
