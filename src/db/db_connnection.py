from abc import ABC, abstractmethod
from typing import Any, Optional, Literal, overload


class DbConnection(ABC):
    """Abstract class for database connection"""

    def __init__(self):
        pass

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    @overload
    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None, single: Literal[False] = False) -> Optional[list[tuple]]:
        pass

    @abstractmethod
    @overload
    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None, single: Literal[True] = True) -> Optional[tuple]:
        pass

    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None, single: bool = False) -> Optional[list[tuple] | tuple]:
        pass

    @abstractmethod
    def execute_mutation(self, query: str, params: Optional[tuple[Any, ...]] = None) -> bool:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
