from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
__all__ = [
    'Base',
    'Client',
]



class Base(DeclarativeBase):
    pass


class Client(Base):
    """ClientModel class to handle the client model.

    Attributes:
    __tablename__ (str): The name of the table
    id (int): The id of the client
    ci (str): The cedula of the client
    name (str): The name of the client
    phone (str): The phone of the client
    last_state (str): The last state of the client
    saraguros_id (int): The id of the client in saragurosnet
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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, ci={self.ci}, name={self.names}, lastnames={self.lastnames}, phone={self.phone}, last_state={self.last_state}, saraguros_id={self.saraguros_id}, created_at={self.created_at}, updated_at={self.updated_at})>"


