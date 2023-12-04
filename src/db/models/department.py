from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base, ITimeControl

if TYPE_CHECKING:
    from src.common.models.user import User
    from src.db.models.ticket import Ticket


class DepartmentIdEnum(str, Enum):
    """DepartmentIdEnum class to handle the department id enum.

    Attributes:
    SUPPORT (str): The support department id
    SALES (str): The sales department id
    CLAIMS (str): The claims department id
    """

    SUPPORT = "SUPPORT"
    SALES = "SALES"
    CLAIMS = "CLAIMS"


class Department(Base, ITimeControl):
    """Department class to handle the department model.

    Attributes:
    id (str): The id of the department
    name (str): The name of the department
    external_id (int): The external id of the Saragurosnet department
    created_at (datetime): The datetime when the department was created
    updated_at (datetime): The datetime when the department was updated
    """

    __tablename__ = "departments"

    id: Mapped[str] = mapped_column(String(10), nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    external_id: Mapped[int] = mapped_column(Integer, nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="department")
    users: Mapped[list["User"]] = relationship(back_populates="department")

    def __repr__(self) -> str:
        return f"<DepartmentModel(id={self.id}, name={self.name}, external_id={self.external_id}, created_at={self.created_at}, updated_at={self.updated_at})>"
