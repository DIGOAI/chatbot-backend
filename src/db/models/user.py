from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import Enum as EnumType
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.models import SystemRole
from src.db.models.base import Base, ITimeControl, IUuidPk

if TYPE_CHECKING:
    from src.db.models.job_role import JobRole


class User(Base, IUuidPk, ITimeControl):
    """UserModel class to handle the user model.

    Attributes:
    __tablename__ (str): The name of the table
    id (int): The id of the user
    email (str): The email of the user
    password (str): The password of the user
    names (str): The names of the user
    lastnames (str): The lastnames of the user
    system_role (str): The system role of the user
    active (bool): The active status of the user
    created_at (datetime): The datetime when the user was created
    updated_at (datetime): The datetime when the user was updated
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    names: Mapped[Optional[str]] = mapped_column(String(40), nullable=True, default=None, server_default=None)
    lastnames: Mapped[Optional[str]] = mapped_column(String(40), nullable=True, default=None, server_default=None)
    system_role: Mapped[SystemRole] = mapped_column(EnumType(SystemRole), default=SystemRole.WORKER)
    job_role_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey(
        "job_roles.id", ondelete="CASCADE"), nullable=True, default=None, server_default=None)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")

    job_role: Mapped["JobRole"] = relationship(back_populates="users")
    # company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    # company: Mapped["Company"] = relationship(cascade="all,delete", back_populates="workers")

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, email={self.email}, password={self.password}, names={self.names}, lastnames={self.lastnames}, system_role={self.system_role}, job_role={self.job_role}, active={self.active}, created_at={self.created_at}, updated_at={self.updated_at})>"
