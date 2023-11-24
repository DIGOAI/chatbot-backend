from src.common.cases import OptionsUseCases as _options_cases
from src.common.logger import Logger
from src.crons.data_reconciliation import (
    data_reconciliation_process as _data_reconciliation_process,
)
from src.crons.schedule_thread import ScheduleManager as _ScheduleManager
from src.crons.service_expiration import (
    service_close_to_expiration as _service_close_to_expiration,
)

ScheduleManager = _ScheduleManager(interval=5)

try:
    options = _options_cases().get_options()

    ScheduleManager.add_job(_service_close_to_expiration,  # type: ignore
                            day=options.cutting_day,
                            hour=options.cutting_hour.strftime("%H:%M"))
    ScheduleManager.add_job(_data_reconciliation_process,  # type: ignore
                            interval=options.data_reconciliation_interval,
                            hour=options.data_reconciliation_hour.strftime("%H:%M"))

except Exception as e:
    Logger.error(err=e)

__all__ = [
    "ScheduleManager",
]
