from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.db.models.base import Base, ITimeControl, IUuidPk
from src.api.db.models.department import Department

if TYPE_CHECKING:
    from src.api.db.models.user import User


class JobRole(Base, IUuidPk, ITimeControl):
    """JobRole class to handle the job role model.

    Attributes:
    id (uuid): The id of the job role
    name (str): The name of the job role
    external_id (int): The external id of the Saragurosnet job role
    created_at (datetime): The datetime when the job role was created
    updated_at (datetime): The datetime when the job role was updated
    """

    __tablename__ = "job_roles"

    name: Mapped[str] = mapped_column(String(80), nullable=False)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)

    department: Mapped["Department"] = relationship(back_populates="job_roles")
    users: Mapped[list["User"]] = relationship(back_populates="job_role")

    def __repr__(self) -> str:
        return f"<JobRoleModel(id={self.id}, name={self.name}, department_id={self.department_id}, created_at={self.created_at}, updated_at={self.updated_at})>"
