from enum import Enum
from typing import Callable, Generic, TypeVar, cast

from typing_extensions import Protocol

from src.common.logger import Logger

T = TypeVar('T', contravariant=True)

ActionFunctionReturnType = None | list[str] | str | bool | tuple[str, bool] | tuple[list[str], bool]


class ActionStatus(Enum):
    SKIPPED = 0
    EXECUTED = 1


class PreActionFunction(Generic[T], Protocol):
    def __call__(self, ctx: T) -> None:
        ...


class ActionFunction(Generic[T], Protocol):
    def __call__(self, ctx: T, id_func: str) -> ActionFunctionReturnType:
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

    def __call__(self, context: T) -> tuple[bool, ActionStatus, list[str] | str]:
        if self._condition(context):
            func_name = cast(Callable[[T], None], self._func).__name__
            Logger.debug(f"Executing action {self.id} - {func_name}")

            res = self._func(context, self.id)

            if isinstance(res, tuple):
                next_actions, continue_ = res
                return continue_, ActionStatus.EXECUTED, next_actions

            if isinstance(res, bool):
                return res, ActionStatus.EXECUTED, self.next

            if isinstance(res, str) or isinstance(res, list):
                return self._end, ActionStatus.EXECUTED, res

            return self._end, ActionStatus.EXECUTED, self.next

        else:
            Logger.debug(f"Condition is False, skipping action {self.id}")
            return False, ActionStatus.SKIPPED, self.next
