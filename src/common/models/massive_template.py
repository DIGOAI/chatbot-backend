from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import Field

from src.common.models.base import BaseModel


class MassiveTemplateType(str, Enum):
    """MassiveTemplateType class to handle the massive template type enum.

    Attributes:
    EMAIL (str): The email massive template type
    SMS (str): The sms massive template type
    WHATSAPP (str): The whatsapp massive template type
    """

    EMAIL = "EMAIL"
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"


class MassiveTemplateResume(BaseModel):
    """MassiveTemplateResume class to handle the massive template resume model.

    Attributes:
    id (UUID): The id of the massive template
    name (str): The name of the massive template
    description (str): The description of the massive template
    type (MassiveTemplateType): The type of the massive template
    """

    id: UUID
    name: str
    description: Optional[str]
    type: MassiveTemplateType

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "e6a3f1c4-9a9b-4f9c-9b7c-5f1b4a9c8f5c",
                "name": "Massive template name",
                "description": "Massive template description",
                "type": "EMAIL"
            }
        }
    }


class MassiveTemplateBase(BaseModel):
    """MassiveTemplateBase class to handle the massive template base model.

    Attributes:
    name (str): The name of the massive template
    description (str): The description of the massive template
    type (MassiveTemplateType): The type of the massive template
    data (dict[str, Any]): The data of the massive template
    template (str): The template of the massive template
    """

    name: str = Field(..., max_length=80)
    description: Optional[str] = Field(None, max_length=255)
    type: MassiveTemplateType
    data: dict[str, Any]
    template: str

    model_config = {
        "from_attributes": True
    }


class MassiveTemplateInsert(MassiveTemplateBase):
    """MassiveTemplateInsert class to handle the massive template insert model.

    Attributes:
    name (str): The name of the massive template
    description (str): The description of the massive template
    type (MassiveTemplateType): The type of the massive template
    data (dict[str, Any]): The data of the massive template
    template (str): The template of the massive template
    """

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "name": "Massive template name",
                "description": "Massive template description",
                "type": "EMAIL",
                "data": {
                    "subject": "Massive template subject",
                    "body": "Massive template body"
                },
                "template": "<html><body><h1>Massive template body</h1></body></html>",
            }
        }
    }


class MassiveTemplate(MassiveTemplateBase):
    """MassiveTemplate class to handle the massive template model.

    Attributes:
    id (UUID): The id of the massive template
    name (str): The name of the massive template
    description (str): The description of the massive template
    type (MassiveTemplateType): The type of the massive template
    data (dict[str, Any]): The data of the massive template
    template (str): The template of the massive template
    created_at (datetime): The datetime when the massive template was created
    updated_at (datetime): The datetime when the massive template was updated
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "e6a3f1c4-9a9b-4f9c-9b7c-5f1b4a9c8f5c",
                "name": "Massive template name",
                "description": "Massive template description",
                "type": "EMAIL",
                "data": {
                    "subject": "Massive template subject",
                    "body": "Massive template body"
                },
                "template": "<html><body><h1>Massive template body</h1></body></html>",
                "created_at": "2021-08-29T19:40:00.000Z",
                "updated_at": "2021-08-29T19:40:00.000Z"
            }
        }
    }
