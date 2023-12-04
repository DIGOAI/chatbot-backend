from typing import Any, Generic, List, Literal, Optional, Sequence, TypeVar, overload
from uuid import UUID

from sqlalchemy import ColumnExpressionArgument, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql._typing import _DMLColumnKeyMapping  # type: ignore

from src.common.models.base import BaseModel
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

    @overload
    def add(self, data: dict[str, Any], return_: Literal[True] = True) -> PyModel:
        ...

    @overload
    def add(self, data: dict[str, Any], return_: Literal[False]) -> bool:
        ...

    def add(self, data: dict[str, Any], return_: bool = True) -> PyModel | bool:
        model = self.db_model(**data)
        self.session.add(model)
        self.session.commit()

        if return_:
            self.session.refresh(model)
            model_created = self.py_model.model_validate(model)

            return model_created

        return True

    def get(self, id: int | UUID) -> PyModel:
        model = self.session.get(self.db_model, id)

        if not model:
            raise IdNotFoundError(id)

        return self.py_model.model_validate(model)

    def list(self, from_: Optional[int] = None, to: Optional[int] = None) -> list[PyModel]:
        stmt = select(self.db_model).limit(to).offset(from_)
        models = self.session.scalars(stmt).all()
        return [self.py_model.model_validate(model) for model in models]

    def delete(self, id: int | UUID) -> PyModel:
        model = self.session.get(self.db_model, id)

        if not model:
            raise IdNotFoundError(id)

        self.session.delete(model)
        self.session.commit()
        return self.py_model.model_validate(model)

    @overload
    def filter(self, *expresions: ColumnExpressionArgument[bool], first: Literal[False] = False) -> List[PyModel]:
        ...

    @overload
    def filter(self, *expresions: ColumnExpressionArgument[bool], first: Literal[True] = True) -> PyModel | None:
        ...

    def filter(self, *expresions: ColumnExpressionArgument[bool], first: bool = False) -> List[PyModel] | Optional[PyModel]:
        stmt = select(self.db_model)

        if expresions:
            stmt = stmt.where(*expresions)

        if first:
            model = self.session.scalars(stmt).first()
            if not model:
                return None
            return self.py_model.model_validate(model)

        models = self.session.scalars(stmt).all()
        return [self.py_model.model_validate(model) for model in models]

    def update(self, id: int | UUID, *values: _DMLColumnKeyMapping[Any] | Sequence[Any], **kwvalues: Any) -> PyModel:
        stmt = (
            update(self.db_model)
            .where(self.db_model.id == id)  # type: ignore
            .values(*values, **kwvalues)
            .returning(self.db_model)
        )

        model_updated = self.session.scalars(stmt).one()
        self.session.commit()

        return self.py_model.model_validate(model_updated)
