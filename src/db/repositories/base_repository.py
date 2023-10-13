from typing import Any, Generic, Sequence, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import BinaryExpression, select, update
from sqlalchemy.orm import Session

from src.db.models import Base

DbModel = TypeVar('DbModel', bound=Base)
PyModel = TypeVar('PyModel', bound=BaseModel)


class IdNotFoundError(Exception):
    """Raised when the id is not found in the database.

    Attributes:
    id (int | UUID): id that was not found
    message (str): explanation of the error
    """

    def __init__(self, id: int | UUID, message: str = "Row with {id} ID not found") -> None:
        self.id = id
        self.message = message.format(id=id)
        super().__init__(self.message)


class BaseRepository(Generic[DbModel, PyModel]):
    """BaseRepository class to handle the database operations.

    Attributes:
    db_model (type[DbModel]): The database model
    py_model (type[PyModel]): The pydantic model
    session (Session): The database session
    """

    def __init__(self, db_model: type[DbModel], py_model: type[PyModel], session: Session):
        self.db_model = db_model
        self.py_model = py_model
        self.session = session

    def add(self, data: dict[str, Any]) -> PyModel:
        model = self.db_model(**data)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        model_created = self.py_model.model_validate(model)

        return model_created

    def get(self, id: int | UUID) -> PyModel:
        # stmt = select(self.db_model).where(self.db_model.id == id)
        # model = self.session.scalars(stmt).first()
        # return self.session.query(self.db_model).filter(self.db_model.id == id).first()
        model = self.session.get(self.db_model, id)

        if not model:
            raise IdNotFoundError(id)

        return self.py_model.model_validate(model)

    def list(self) -> list[PyModel]:
        stmt = select(self.db_model)
        models = self.session.scalars(stmt).all()

        return [self.py_model.model_validate(model) for model in models]

    def delete(self, id: int | UUID) -> PyModel:
        model = self.get(id)
        self.session.delete(model)
        self.session.commit()
        return model

    def filter(self, *expresions: BinaryExpression[Any]):
        stmt = select(self.db_model)

        if expresions:
            stmt = stmt.where(*expresions)

        models = self.session.scalars(stmt).all()

        return [self.py_model.model_validate(model) for model in models]

    def update(self, id: int | UUID, *values: Sequence[Any]) -> PyModel:
        stmt = (
            update(self.db_model)
            .where(self.db_model.id == id)  # type: ignore
            .values(*values)
            .returning(self.db_model)
        )

        model_updated = self.session.scalars(stmt).one()
        self.session.commit()

        return self.py_model.model_validate(model_updated)
