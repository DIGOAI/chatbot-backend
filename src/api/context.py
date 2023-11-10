from contextlib import asynccontextmanager

from fastapi import FastAPI as _FastAPI

from src.common.logger import Logger
from src.crons import ScheduleManager as _schedule_manager


@asynccontextmanager
async def lifespan(app: _FastAPI):
    # Execute startup procedure
    Logger.info("Starting application startup procedures")
    _schedule_manager.run_schedules_continuously()
    Logger.info("Started schedules thread")

    yield  # Run application

    # Execute shutdown procedure
    Logger.info("Cleanning application startup procedures")

    await _schedule_manager.stop_schedules_continuously()
    Logger.info("Stopped schedules thread")
