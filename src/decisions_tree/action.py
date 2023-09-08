from typing import Callable, Generic, Optional, TypedDict, TypeVar, cast

from typing_extensions import Protocol

from src.logger import Logger

T = TypeVar('T', contravariant=True)


class ActionFunction(Generic[T], Protocol):
    def __call__(self, context: T) -> None:
        ...


class Action(Generic[T]):
    """Action class.

    This class represents an generic action to execute.

    Parameters:
    id (str): The id of the action
    func (Callable[[T], None]): The function to execute
    """

    def __init__(self, id: str, func: ActionFunction[T], condition: Optional[bool] = None, end: bool = True) -> None:
        self.id = id
        self._func = func
        self._condition = condition
        self._end = end

    def __call__(self, context: T) -> bool:
        if self._condition is None or self._condition:
            Logger.info(
                f"Executing action {self.id} - {cast(Callable[[T], None], self._func).__name__}")
            self._func(context)
            return not self._end
        else:
            Logger.info(f"Condition is False, skipping action {self.id}")
            return True


if __name__ == "__main__":
    ContextType = TypedDict('ContextType', {
        'user_id': str,
        'user_ci': str,
        'status': int
    })

    context: ContextType = {
        'user_id': 'dsad234',
        'user_ci': '123456789',
        'status': 4
    }

    def print_context(context: ContextType) -> None:
        print(context)

    action = Action("1.0",  print_context)

    action(context)
