import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class InsuficientDataError(Exception):
    """The exception raised when the data is not enough to process the request."""

    message: str = "Cannot create a JSON due to insufficient or incorrect data: {data}"

    def __init__(self, data: dict[str, Any] | str) -> None:
        super().__init__(self.message.format(data=data))


class ReceibeData(BaseModel):
    """The data extracted from a receipt.

    Attributes:
    bank (str): The bank where the transaction was made.
    customer (str): The name of the customer.
    date (str): The date of the transaction.
    hour (str): The hour of the transaction.
    currency (str): The currency of the transaction.
    total (float): The total amount of the transaction.
    """

    bank: Optional[str] = Field(...)
    customer: Optional[str] = Field(...)
    date: Optional[datetime.date] = Field(...)
    hour: Optional[datetime.time] = Field(...)
    currency: Optional[str] = Field(...)
    total: Optional[float] = Field(...)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "bank": "Banco de Loja",
                    "customer": "John Doe",
                    "date": "2021-01-01",
                    "hour": "12:00",
                    "currency": "USD",
                    "total": 100.0,
                }
            ]
        }
    }
