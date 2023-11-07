import re

import pytz
import schedule

from src.common.utils import HOUR_PATTERN as _HOUR_PATTERN

_hour_matcher = re.compile(_HOUR_PATTERN)


def service_close_to_expiration(day: int, hour: str, tz: str = "America/Guayaquil") -> schedule.Job:
    """Schedule a task to execute at a specific time.

    Atributes:
    day (int): The day of the month to execute the task
    hour (str): The hour of the day to execute the task (format: HH:MM)
    tz (str): The timezone to execute the task (default: America/Guayaquil)
    """

    def task():
        """Task to execute"""

        from datetime import datetime as dt

        today = dt.now(pytz.timezone(tz)).day

        if today == day:
            print(f"Service close to expiration: {day}")

    if day > 31 or day < 1:
        raise ValueError("The day must be between 1 and 31")

    if not _hour_matcher.match(hour):
        raise ValueError("The hour must be a valid time in format HH:MM")

    if tz not in pytz.all_timezones:
        raise ValueError("The timezone must be a valid timezone")

    return schedule.every().day.at(hour, tz).do(task)  # type: ignore
