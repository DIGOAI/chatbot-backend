from abc import ABC, abstractmethod
from typing import (Any, Literal, LiteralString, Mapping, Optional, Self,
                    Sequence, Type, TypeVar, overload)

T = TypeVar('T')


class DbConnection(ABC):
    """Abstract class for database connection"""

    def __init__(self):
        ...

    @abstractmethod
    def __enter__(self) -> Self:
        ...

    @abstractmethod
    @overload
    def execute_query(self, query: LiteralString, params: Optional[Sequence[Any] | Mapping[str, Any]] = None, bound: Type[T] = Type, single: Literal[False] = False) -> list[T]:
        ...

    @abstractmethod
    @overload
    def execute_query(self, query: LiteralString, params: Optional[Sequence[Any] | Mapping[str, Any]] = None, bound: Type[T] = Type, single: Literal[True] = True) -> T | None:
        ...

    @abstractmethod
    def execute_query(self, query: LiteralString, params: Optional[Sequence[Any] | Mapping[str, Any]] = None, bound: Type[T] = Type, single: bool = False) -> list[T] | T | None:
        ...

    @abstractmethod
    def execute_mutation(self, query: LiteralString, params: Optional[Sequence[Any] | Mapping[str, Any]] = None,) -> bool:
        ...

    @abstractmethod
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[Any]) -> None:
        ...
