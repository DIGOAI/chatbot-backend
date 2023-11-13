import re

import pytz
import schedule

from src.common.logger import Logger
from src.common.utils import HOUR_PATTERN as _HOUR_PATTERN

_hour_matcher = re.compile(_HOUR_PATTERN)


def data_reconciliation_process(interval: int, hour: str, tz: str = "America/Guayaquil") -> schedule.Job:
    """Schedule a task to execute at a specific time.

    Atributes:
    interval (int): The interval in days to execute the task
    hour (str): The hour of the day to execute the task (format: HH:MM)
    tz (str): The timezone to execute the task (default: America/Guayaquil)
    """

    def task():
        """Task to execute"""

        from datetime import datetime as dt

        today = dt.now(pytz.timezone(tz)).strftime("%d/%m/%Y")
        Logger.info(f"Fetching data from {interval} days ago at {today} {hour} in {tz}")

    if interval < 1 or interval > 10:
        raise ValueError("The intervas in days must be between 1 and 10")

    if not _hour_matcher.match(hour):
        raise ValueError("The hour must be a valid time in format HH:MM")

    if tz not in pytz.all_timezones:
        raise ValueError("The timezone must be a valid timezone")

    Logger.info(
        f"Data reconciliation process scheduled at {interval} days {hour} in {tz}", "reconciliation job")

    return schedule.every(interval).days.at(hour, tz).do(task)  # type: ignore
