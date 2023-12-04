from datetime import datetime, time
from typing import Optional
from uuid import UUID

from pydantic import Field

from src.common.models.base import BaseModel


class OptionsBase(BaseModel):
    """OptionsBase class to handle the options model.

    Attributes:
    cutting_day (int): The cutting day of the options (1-31)
    cutting_hour (str): The cutting hour of the options (HH:MM)
    data_reconciliation_interval (int): The data reconciliation interval of the options (1-5)
    data_reconciliation_hour (str): The data reconciliation hour of the options (HH:MM)
    """

    cutting_day: int = Field(..., ge=1, le=31)
    cutting_hour: time = Field(...)
    data_reconciliation_interval: int = Field(..., ge=1, le=5)
    data_reconciliation_hour: time = Field(...)

    model_config = {
        "from_attributes": True
    }


class OptionsUpdate(OptionsBase):
    """OptionsUpdate class to handle the options model.

    Attributes:
    cutting_day (int): The cutting day of the options (1-31)
    cutting_hour (str): The cutting hour of the options (HH:MM)
    data_reconciliation_interval (int): The data reconciliation interval of the options (1-5)
    data_reconciliation_hour (str): The data reconciliation hour of the options (HH:MM)
    """

    cutting_day: Optional[int] = Field(None, ge=1, le=31)  # type: ignore
    cutting_hour: Optional[time] = Field(None)  # type: ignore
    data_reconciliation_interval: Optional[int] = Field(None, ge=1, le=5)  # type: ignore
    data_reconciliation_hour: Optional[time] = Field(None)  # type: ignore

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "cutting_day": 1,
                "cutting_hour": "00:00",
                "data_reconciliation_interval": 1,
                "data_reconciliation_hour": "00:00"
            }
        }
    }


class Options(OptionsBase):
    """Options class to handle the options model.

    Attributes:
    id (uuid): The id of the options
    cutting_day (int): The cutting day of the options (1-31)
    cutting_hour (str): The cutting hour of the options (HH:MM)
    data_reconciliation_interval (int): The data reconciliation interval of the options (1-5)
    data_reconciliation_hour (str): The data reconciliation hour of the options (HH:MM)
    created_at (datetime): The datetime when the options was created
    updated_at (datetime): The datetime when the options was updated
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "00000000-0000-0000-0000-000000000000",
                "cutting_day": 1,
                "cutting_hour": "00:00",
                "data_reconciliation_interval": 1,
                "data_reconciliation_hour": "00:00",
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00"
            }
        }
    }
