from datetime import datetime
from uuid import UUID

from src.common.cases.base_use_cases import UseCaseBase
from src.common.models import Options, OptionsUpdate
from src.crons.data_reconciliation import (
    data_reconciliation_process as _data_reconciliation_process,
)
from src.crons.service_expiration import (
    service_close_to_expiration as _service_close_to_expiration,
)
from src.db.models import Options as OptionsModel
from src.db.repositories import BaseRepository


class OptionsUseCases(UseCaseBase):

    def get_options(self):
        with self._session() as session:
            options_repo = BaseRepository(OptionsModel, Options, session)
            options = options_repo.list()

        if options:
            return options[0]
        else:
            raise Exception("No options founded")

    def update_options(self, options_id: UUID, options_data: OptionsUpdate):
        data = options_data.model_dump(exclude_unset=True)
        data["updated_at"] = datetime.utcnow()

        with self._session() as session:
            options_repo = BaseRepository(OptionsModel, Options, session)
            options = options_repo.update(options_id, **data)

        # Stop jobs
        from src.crons import ScheduleManager
        ScheduleManager.stop_schedules_continuously()

        # Set new jobs updated
        ScheduleManager.clear_jobs()
        ScheduleManager.add_job(_service_close_to_expiration,  # type: ignore
                                day=options.cutting_day,
                                hour=options.cutting_hour.strftime("%H:%M"))
        ScheduleManager.add_job(_data_reconciliation_process,  # type: ignore
                                interval=options.data_reconciliation_interval,
                                hour=options.data_reconciliation_hour.strftime("%H:%M"))

        # Start jobs
        ScheduleManager.run_schedules_continuously()

        return options
