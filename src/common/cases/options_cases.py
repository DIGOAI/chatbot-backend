from datetime import datetime
from uuid import UUID

from src.common.cases.base_use_cases import UseCaseBase
from src.common.models import Options, OptionsUpdate
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

        return options
