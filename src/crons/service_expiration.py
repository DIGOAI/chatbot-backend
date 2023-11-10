import re

import pytz
import schedule

from src.common.logger import Logger
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

        today = dt.now(pytz.timezone(tz))
        today_str = today.strftime("%d/%m/%Y")
        today_day = today.day

        if today_day == day:
            Logger.info(
                f"Sending email alert of service close to expiration at {today_str} {hour} in {tz}")

    if day > 31 or day < 1:
        raise ValueError("The day must be between 1 and 31")

    if not _hour_matcher.match(hour):
        raise ValueError("The hour must be a valid time in format HH:MM")

    if tz not in pytz.all_timezones:
        raise ValueError("The timezone must be a valid timezone")

    Logger.info(f"Service close to expiration scheduled at {day} {hour} in {tz}", "expiration job")

    return schedule.every().days.at(hour, tz).do(task)  # type: ignore
