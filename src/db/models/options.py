from sqlalchemy.dialects.postgresql import SMALLINT, TIME
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base, ITimeControl, IUuidPk


class Options(Base, IUuidPk, ITimeControl):
    """Options class to handle the options model.

    Attributes:
    id (uuid): The id of the options
    cutting_day (int): The cutting day of the options
    cutting_hour (str): The cutting hour of the options (HH:MM)
    data_reconciliation_interval (int): The data reconciliation interval of the options
    data_reconciliation_hour (str): The data reconciliation hour of the options (HH:MM)
    created_at (datetime): The datetime when the options was created
    updated_at (datetime): The datetime when the options was updated
    """
    __tablename__ = "options"

    cutting_day: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=1, server_default="1")
    cutting_hour: Mapped[str] = mapped_column(TIME, nullable=False, default="00:00", server_default="00:00")
    data_reconciliation_interval: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=1, server_default="1")
    data_reconciliation_hour: Mapped[str] = mapped_column(TIME, nullable=False, default="00:00", server_default="00:00")

    def __repr__(self) -> str:
        return f"<Options(id={self.id}, cutting_day={self.cutting_day}, cutting_hour={self.cutting_hour}, data_reconciliation_interval={self.data_reconciliation_interval}, created_at={self.created_at}, updated_at={self.updated_at})>"
