from functools import wraps
from typing import Callable, Generic, Optional, TypeVar, cast

from src.chatbot.decisions_tree.action import (
    Action,
    ActionFunction,
    ActionStatus,
    PreActionFunction,
)
from src.common.logger import Logger

T = TypeVar('T')


class DecisionsTree(Generic[T]):
    """DecisionsTree class.

    This class represents a decisions tree to execute actions.

    Parameters:
    context (T): The context to use in the actions
    start_id (str): The id of the action to start
    """

    def __init__(self, context: Optional[T] = None, start_id: str = "0.1") -> None:
        self._tree: dict[str, Action[T]] = {}
        self.context = context or cast(T, {})
        self._start_id = start_id
        self._preactions: list[PreActionFunction[T]] = []

    @property
    def context(self) -> T:
        return self.__context

    @context.setter
    def context(self, context: T) -> None:
        self.__context = context

    def add_preaction(self):
        """Add a preaction to the tree.

        The preaction is a function that will be executed before the actions.

        Returns:
        Callable[[PreActionFunction[T]], None]: The decorator to add the preaction
        """

        def inner_decorator(func: PreActionFunction[T]):
            @wraps(func)
            def wrapper():
                self._preactions.append(func)

            return wrapper()
        return inner_decorator

    def add_action(self, id: str, condition: Callable[[T], bool], end: bool = True, next: str | list[str] = []):
        """Add an action to the tree.

        The action is a function that will be executed if the condition is true.

        Attributes:
        id (str): The id of the action
        condition (Callable[[T], bool]): The condition to execute the action
        end (bool): If the action is the last one
        next (str | list[str]): The next action to execute
        """

        def inner_decorator(func: ActionFunction[T]):
            @wraps(func)
            def wrapper():
                self._tree[id] = Action(id, func, condition, end, next)

            return wrapper()
        return inner_decorator

    def __call__(self, next_actions: str | list[str] | None) -> str | list[str] | None:
        """Build and execute the actions.

        When the actions are executed, the preactions are executed before the actions.
        The actions are executed until the end is reached.

        Attributes:
        next_actions (str | list[str] | None): The next actions to execute
        """

        Logger.info(f"Building and executing actions")

        ended = False
        preactions_executed = False
        next_actions_to_execute: str | list[str] | None = None

        # Execute the actions until the end is reached
        while not ended:

            # If the next actions is None, set the start action
            if next_actions is None:
                next_actions = []

            # If the next actions is a string, convert to a list
            if isinstance(next_actions, str):
                next_actions = [next_actions]

            # If the next actions is empty, set the start action
            if not next_actions:
                next_actions = [self._start_id]

            # If preactions are not executed, execute them
            if not preactions_executed:
                # Execute the preactions
                for preaction in self._preactions:
                    Logger.info(f"Executing preaction {preaction.__name__}")  # type: ignore
                    preaction(self.context)

                # Set the preactions as executed
                preactions_executed = True

            # Execute the actions
            for id in next_actions:
                # If the action is not found, raise an error
                if id not in self._tree:
                    raise ValueError(f"Action {id} not found")

                # Execute the action
                action = self._tree[id]
                ended, status = action(self.context)

                # If the action is ended or executed, set the next actions to execute
                if ended or status == ActionStatus.EXECUTED:
                    next_actions_to_execute = action.next
                    break

                # Set the next actions to execute
                next_actions_to_execute = action.next

            next_actions = next_actions_to_execute

        Logger.info(f"Finished building and executing actions")
        return next_actions_to_execute  # Return the next actions to execute
