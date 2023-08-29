from typing import Callable, Generic, TypedDict, TypeVar

from typing_extensions import Protocol

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

    def __init__(self, id: str, func: ActionFunction[T]) -> None:
        self.id = id
        self._func = func

    def __call__(self, context: T) -> None:
        self._func(context)


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
