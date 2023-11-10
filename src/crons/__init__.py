from src.crons.data_reconciliation import (
    data_reconciliation_process as _data_reconciliation_process,
)
from src.crons.schedule_thread import ScheduleManager as _ScheduleManager
from src.crons.service_expiration import (
    service_close_to_expiration as _service_close_to_expiration,
)

ScheduleManager = _ScheduleManager(interval=5)

ScheduleManager.add_job(_service_close_to_expiration, day=10, hour="11:38")  # type: ignore
ScheduleManager.add_job(_data_reconciliation_process, interval=1, hour="11:39")  # type: ignore

__all__ = [
    "ScheduleManager",
]
