from enum import Enum


class AlertType(str, Enum):
    """Enum for the alert types."""

    ERROR = "ERR"
    WARNING = "WAR"
    ALERT = "ALE"
    INFO = "INF"
    DEBUG = "DEB"

    def __str__(self) -> str:
        return self.value
