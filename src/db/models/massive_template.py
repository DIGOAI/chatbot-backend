from enum import Enum
from typing import Any

from sqlalchemy import Enum as EnumType
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base, ITimeControl, IUuidPk


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


class MassiveTemplate(Base, IUuidPk, ITimeControl):
    """MassiveTemplate class to handle the massive template model.

    Attributes:
    id (uuid): The id of the massive template
    name (str): The name of the massive template
    description (str): The description of the massive template
    type (MassiveTemplateType): The type of the massive template
    created_at (datetime): The datetime when the massive template was created
    updated_at (datetime): The datetime when the massive template was updated
    """

    __tablename__ = "massive_templates"

    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    type: Mapped[MassiveTemplateType] = mapped_column(EnumType(MassiveTemplateType), nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    def __repr__(self) -> str:
        return f"<MassiveTemplateModel(id={self.id}, name={self.name}, description={self.description}, type={self.type}, created_at={self.created_at}, updated_at={self.updated_at})>"
