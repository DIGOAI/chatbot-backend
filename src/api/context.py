from contextlib import asynccontextmanager

import schedule
from fastapi import FastAPI as _FastAPI

from src.common.logger import Logger
from src.crons import run_schedules_continuously as _run_schedules_continuously
from src.crons import service_close_to_expiration as _service_close_to_expiration


@asynccontextmanager
async def lifespan(app: _FastAPI):
    # Execute startup procedure
    Logger.info("Starting events")
    # TODO: Change the day and hour to a value from the database
    _expiration_job = _service_close_to_expiration(30, "10:00")
    _schedules_thread = _run_schedules_continuously()

    yield  # Run application

    # Execute shutdown procedure
    Logger.info("Stopping schedules thread")
    _schedules_thread.set()
    Logger.info("Stopping expiration job")
    schedule.cancel_job(_expiration_job)
