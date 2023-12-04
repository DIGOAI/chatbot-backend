from datetime import date, datetime, time
from typing import Callable
from uuid import UUID

import pydantic

# Set the serializers for the datetime, date and UUID fields
datetime_serializer: Callable[[datetime], str] = lambda v: v.isoformat()
date_serializer: Callable[[date], str] = lambda v: v.isoformat()
time_serializer: Callable[[time], str] = lambda v: v.strftime('%H:%M')
uuid_serializer: Callable[[UUID], str] = lambda v: str(v)


class BaseModel(pydantic.BaseModel):
    """BaseModel class to handle the base model.

    This class is used to handle the base model with the common configurations.
    Setted the json_encoders to handle the datetime, date and UUID fields.
    """

    model_config = {
        'json_encoders': {
            UUID: uuid_serializer,
            datetime: datetime_serializer,
            date: date_serializer,
            time: time_serializer,
        }
    }
