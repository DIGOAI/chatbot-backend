import threading
from typing import Any, NamedTuple, Protocol, Self

import schedule


class ScheduleFunction(Protocol):
    def __call__(self, **kwargs: Any) -> schedule.Job: ...


class JobData(NamedTuple):
    job_func: ScheduleFunction
    job_params: dict[str, Any]


class ScheduleManager:
    _instance: Self | None = None
    _cease_continuous_run: threading.Event
    _interval: int
    _continuous_thread: "ScheduleManager.ScheduleThread"
    _jobs_for_run: list[JobData] = []
    _jobs_running: list[schedule.Job] = []

    def __new__(cls, interval: int = 1) -> "ScheduleManager":
        if cls._instance is None:
            cls._instance = super(ScheduleManager, cls).__new__(cls)
            cls._instance._cease_continuous_run = threading.Event()
            cls._instance._interval = interval
            cls._instance._continuous_thread = cls._instance.ScheduleThread()

        return cls._instance

    def _init_jobs(self) -> None:
        for job_func, job_params in self._jobs_for_run:
            self._jobs_running.append(job_func(**job_params))

    def _stop_jobs(self) -> None:
        for job in self._jobs_running:
            schedule.cancel_job(job)

    def add_job(self, job_func: ScheduleFunction, **job_params: Any) -> None:
        self._jobs_for_run.append(JobData(job_func, job_params))

    def clear_jobs(self) -> None:
        self._jobs_for_run = []

    def run_schedules_continuously(self) -> None:
        if self._instance is None:
            raise ValueError("The ScheduleManager is not initialized")

        # Initialize jobs
        self._instance._init_jobs()

        # self._instance._interval = interval
        if not self._instance._continuous_thread.is_alive():
            self._instance._continuous_thread.start()

    def stop_schedules_continuously(self):
        if self._instance is None:
            raise ValueError("The ScheduleManager is not initialized")

        # Stop jobs
        self._instance._stop_jobs()

        self._instance._cease_continuous_run.set()
        self._instance._continuous_thread.join()

        self._instance._continuous_thread = self._instance.ScheduleThread()
        self._instance._cease_continuous_run.clear()

    class ScheduleThread(threading.Thread):
        """ Class to run scheduled jobs in the background. """

        def __init__(self) -> None:
            """ Initializes the ScheduleThread class. """
            super().__init__(name="ScheduleThread")

        def run(self) -> None:
            if ScheduleManager._instance is None:
                raise ValueError("The ScheduleManager is not initialized")

            while not ScheduleManager._instance._cease_continuous_run.is_set():
                schedule.run_pending()
                seconds_to_next_execution = schedule.idle_seconds()
                # time.sleep(seconds_to_next_execution or ScheduleManager._instance._interval)
                # time.sleep(ScheduleManager._instance._interval)
                ScheduleManager._instance._cease_continuous_run.wait(
                    seconds_to_next_execution or ScheduleManager._instance._interval
                )
