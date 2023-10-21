from functools import wraps
from typing import Any, Callable, Generic, Optional, TypeVar, cast

from src.chatbot.decisions_tree.action import Action, ActionFunction
from src.common.logger import Logger

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
        self._functions: dict[str, Callable[[], None]] = {}

    @property
    def context(self) -> T:
        return self.__context

    @context.setter
    def context(self, context: T) -> None:
        self.__context = context

    def _add_action(self, action: Action[T]) -> None:
        self._tree[action.id] = action

    def add_action(self, id: str, condition: Callable[[T], bool], end: bool = True):
        def inner_decorator(func: ActionFunction[T]):
            @wraps(func)
            def wrapper() -> None:
                self._add_action(
                    Action(id, func, condition(self.context), end))
            self._functions[id] = (wrapper)
            return wrapper
        return inner_decorator

    def __call__(self) -> Any:
        Logger.info(f"Building and executing actions")

        for key, f in self._functions.items():
            f()
            Logger.info(f"Current context: {self.context}")
            if not self._tree[key](self.context):
                break

        Logger.info(f"Finished building and executing actions")
