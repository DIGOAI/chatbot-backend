from abc import ABC, abstractmethod
from typing import Any, Literal, Optional, overload


class DbConnection(ABC):
    """Abstract class for database connection"""

    def __init__(self):
        ...

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    @overload
    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None, single: Literal[False] = False) -> Optional[list[tuple[Any, ...]]]:
        ...

    @abstractmethod
    @overload
    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None, single: Literal[True] = True) -> Optional[tuple[Any, ...]]:
        ...

    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None, single: bool = False) -> Optional[list[tuple[Any, ...]] | tuple[Any, ...]]:
        ...

    @abstractmethod
    def execute_mutation(self, query: str, params: Optional[tuple[Any, ...]] = None) -> bool:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
