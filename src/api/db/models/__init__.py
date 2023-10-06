from src.api.db.models.base import Base
from src.api.db.models.client import Client
from src.api.db.models.department import Department
from src.api.db.models.job_role import JobRole

__all__ = [
    "Base",
    "Department",
    "JobRole",
]


class Base(DeclarativeBase):
    pass


class Client(Base):
    """ClientModel class to handle the client model.

    Attributes:
    __tablename__ (str): The name of the table
    id (int): The id of the client
    ci (str): The cedula of the client
    names (str): The names of the client
    lastnames (str): The lastnames of the client
    phone (str): The phone of the client
    last_state (str): The last state of the client
    saraguros_id (int): The id of the client in saraguros
    created_at (datetime): The datetime when the client was created
    updated_at (datetime): The datetime when the client was updated
    """

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ci: Mapped[str] = mapped_column(String(13), nullable=True)
    names: Mapped[str] = mapped_column(String(40), nullable=True)
    lastnames: Mapped[str] = mapped_column(String(40), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=False)
    last_state: Mapped[str] = mapped_column(String(10), nullable=True)
    saraguros_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    # meta: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    # company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    messages: Mapped[list["Message"]] = relationship(back_populates="client")
    # company: Mapped["Company"] = relationship(cascade="all,delete", back_populates="clients")

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, ci={self.ci}, name={self.names}, lastnames={self.lastnames}, phone={self.phone}, last_state={self.last_state}, saraguros_net={self.saraguros_id}, created_at={self.created_at}, updated_at={self.updated_at})>"


class Message(Base):
    """MessageModel class to handle the message model.

    Attributes:
    __tablename__ (str): The name of the table
    id (int): The id of the message
    message (str): The message of the message
    client_id (int): The id of the client
    created_at (datetime): The datetime when the message was created
    updated_at (datetime): The datetime when the message was updated
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sender: Mapped[str] = mapped_column(String(13), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    client: Mapped["Client"] = relationship(cascade="all,delete", back_populates="messages")

    def __repr__(self) -> str:
        return f"<MessageModel(id={self.id}, sender={self.sender}, message={self.message}, client_id={self.client_id}, created_at={self.created_at})>"


class User(Base):
    """UserModel class to handle the user model.

    Attributes:
    __tablename__ (str): The name of the table
    id (int): The id of the user
    email (str): The email of the user
    password (str): The password of the user
    created_at (datetime): The datetime when the user was created
    updated_at (datetime): The datetime when the user was updated
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    role: Mapped[UserRole] = mapped_column(EnumType(UserRole), default=UserRole.WORKER)
    # company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    # company: Mapped["Company"] = relationship(cascade="all,delete", back_populates="workers")

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, email={self.email}, password={self.password}, created_at={self.created_at}, updated_at={self.updated_at})>"


# class Company(Base):
#     """CompanyModel class to handle the company model.

#     Attributes:
#     __tablename__ (str): The name of the table
#     id (int): The id of the company
#     name (str): The name of the company
#     created_at (datetime): The datetime when the company was created
#     updated_at (datetime): The datetime when the company was updated
#     """

#     __tablename__ = "companies"

#     id: Mapped[int] = mapped_column(String, primary_key=True, index=True)
#     ruc: Mapped[str] = mapped_column(String(13), nullable=False)
#     name: Mapped[str] = mapped_column(String(120), nullable=False)
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

#     workers: Mapped[list["User"]] = relationship(back_populates="company")
#     clients: Mapped[list["Client"]] = relationship(back_populates="company")

#     def __repr__(self) -> str:
#         return f"<CompanyModel(id={self.id}, name={self.name}, created_at={self.created_at}, updated_at={self.updated_at})>"
