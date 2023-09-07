from functools import wraps
from typing import Any, Callable, Generic, Optional, TypeVar, cast

from src.decisions_tree.action import Action, ActionFunction
from src.logger import Logger

T = TypeVar('T')


class DecisionsTree(Generic[T]):
    """DecisionsTree class.

    This class represents a decisions tree to execute actions.

    Parameters:
    context (T): The context to use in the actions
    """

    def __init__(self, context: Optional[T] = None) -> None:
        self._tree: dict[str, Action[T]] = {}
        self.context = context or cast(T, {})
        self._functions: list[Callable[[], None]] = []

    @property
    def context(self) -> T:
        return self.__context

    @context.setter
    def context(self, context: T) -> None:
        self.__context = context

    def _add_action(self, action: Action[T]) -> None:
        self._tree[action.id] = action

    def addActionDecorator(self, id: str, condition: Callable[[T], bool], end: bool = True):
        def inner_decorator(func: ActionFunction[T]):
            @wraps(func)
            def wrapper() -> None:
                self._add_action(
                    Action(id, func, condition(self.context), end))
            self._functions.append(wrapper)
            return wrapper
        return inner_decorator

    def __call__(self) -> Any:
        Logger.info("Building the action tree")
        for func in self._functions:
            func()
        Logger.info(f"Actions: {self._tree.keys()}")

        Logger.info(f"Executing actions")

        for _, action in self._tree.items():
            if not action(self.context):
                break

        Logger.info(f"Finished executing actions")
