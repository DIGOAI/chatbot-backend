from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.db.models.base import Base, ITimeControl, IUuidPk

if TYPE_CHECKING:
    from src.api.db.models.job_role import JobRole


class Department(Base, IUuidPk, ITimeControl):
    """Department class to handle the department model.

    Attributes:
    id (uuid): The id of the department
    name (str): The name of the department
    external_id (int): The external id of the Saragurosnet department
    created_at (datetime): The datetime when the department was created
    updated_at (datetime): The datetime when the department was updated
    """

    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(80), nullable=False)
    external_id: Mapped[int] = mapped_column(Integer, nullable=False)

    job_roles: Mapped[list["JobRole"]] = relationship(back_populates="department")

    def __repr__(self) -> str:
        return f"<DepartmentModel(id={self.id}, name={self.name}, external_id={self.external_id}, job_roles={self.job_roles}, created_at={self.created_at}, updated_at={self.updated_at})>"
