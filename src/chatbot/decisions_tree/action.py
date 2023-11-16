from enum import Enum
from typing import Callable, Generic, Literal, TypeVar, cast

from typing_extensions import Protocol

from src.common.logger import Logger

T = TypeVar('T', contravariant=True)


class ActionStatus(Enum):
    SKIPPED = 0
    EXECUTED = 1


class PreActionFunction(Generic[T], Protocol):
    def __call__(self, ctx: T) -> None:
        ...


class ActionFunction(Generic[T], Protocol):
    def __call__(self, ctx: T, id_func: str) -> None | Literal[False]:
        ...


class Action(Generic[T]):
    """Action class.

    This class represents an generic action to execute.

    Attributes:
    id (str): The id of the action
    func (Callable[[T], None]): The function to execute
    condition (Callable[[T], bool]): The condition to execute the action
    end (bool): If the action is the last one
    """

    def __init__(self, id: str, func: ActionFunction[T], condition: Callable[[T], bool], end: bool = True, next: str | list[str] = []) -> None:
        self.id = id
        self._func = func
        self._condition = condition
        self._end = end
        self.next = next

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: str) -> None:
        self.__id = id

    @property
    def next(self) -> str | list[str]:
        return self.__next

    @next.setter
    def next(self, next: str | list[str]) -> None:
        self.__next = next

    def __call__(self, context: T) -> tuple[bool, ActionStatus]:
        if self._condition(context):
            Logger.info(
                f"Executing action {self.id} - {cast(Callable[[T], None], self._func).__name__}")

            ended = self._func(context, self.id)

            if ended is not None:
                return ended, ActionStatus.EXECUTED

            return self._end, ActionStatus.EXECUTED

        else:
            Logger.info(f"Condition is False, skipping action {self.id}")
            return False, ActionStatus.SKIPPED
