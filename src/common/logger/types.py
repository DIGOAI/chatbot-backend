from enum import Enum


class AlertType(str, Enum):
    """Enum for the alert types."""

    INFO = "INF"
    ERROR = "ERR"
    WARNING = "WAR"
    ALERT = "ALE"
    DEBUG = "DEB"

    def __str__(self) -> str:
        return self.value
