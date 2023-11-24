import os

from src.common.logger.logger import Logger as _Logger

_ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
_log_level = "INFO" if _ENVIRONMENT == "production" else "DEBUG"

Logger = _Logger(_log_level, ["before_cursor_execute"], 25)
