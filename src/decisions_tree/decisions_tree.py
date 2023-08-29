from typing import Any, Generic, TypeVar

from src.decisions_tree.action import Action

T = TypeVar('T')


class DecisionsTree(Generic[T]):
    """DecisionsTree class.

    This class represents a decisions tree to execute actions.

    Parameters:
    context (T): The context to use in the actions
    """

    def __init__(self, context: T) -> None:
        self._tree: dict[str, Action[T]] = {}
        self._context: T = context

    def addAction(self, action: Action[T]) -> None:
        self._tree[action.id] = action

    def __call__(self, status: str) -> Any:
        # Verify if the status is in the tree
        if status not in self._tree:
            print(f"[ERROR][TREE]: Status '{status}' not found in the tree")
            raise Exception(f"Status '{status}' not found in the tree")

        # Execute the action
        self._tree[status](self._context)
