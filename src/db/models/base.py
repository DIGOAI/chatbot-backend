from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ICreatedAt:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now())


class IUpdatedAt:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), server_onupdate=func.now())  # type: ignore


class IUuidPk:
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True,
                                     default=uuid4(), server_default=func.gen_random_uuid())


class ITimeControl(ICreatedAt, IUpdatedAt):
    pass
