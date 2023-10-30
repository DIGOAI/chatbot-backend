from contextlib import asynccontextmanager
from threading import Event

import schedule
from fastapi import FastAPI as _FastAPI

from src.common.logger import Logger
from src.crons import run_schedules_continuously as _run_schedules_continuously
from src.crons import service_close_to_expiration as _service_close_to_expiration

_expiration_job: schedule.Job | None = None
_schedules_thread: Event | None = None


async def startup_event() -> None:
    global _expiration_job, _schedules_thread

    Logger.info("Starting events")
    # TODO: Change the day and hour to a value from the database
    _expiration_job = _service_close_to_expiration(30, "10:00")
    _schedules_thread = _run_schedules_continuously()


async def shutdown_event() -> None:
    global _expiration_job, _schedules_thread

    if _schedules_thread is not None:
        Logger.info("Stopping schedules thread")
        _schedules_thread.set()

    if _expiration_job is not None:
        Logger.info("Stopping expiration job")
        schedule.cancel_job(_expiration_job)


@asynccontextmanager
async def lifespan(app: _FastAPI):
    await startup_event()

    yield

    await shutdown_event()
