from typing import Any, Generic, Type, TypeVar

T = TypeVar('T')


class Singleton(Generic[T]):
    """
    A generic singleton class that ensures only one instance of a class is created.
    """

    _cls: Type[T]
    _instance: T

    def __init__(self, cls: Type[T]) -> None:
        self._cls = cls

    def Instance(self) -> T:
        """
        Returns the instance of the class. If the instance does not exist, it creates a new instance and returns it.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self) -> None:
        """
        Raises a TypeError when trying to access the singleton class directly.
        """
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst: Any) -> bool:
        """
        Checks if an instance is an instance of the class.
        """
        return isinstance(inst, self._cls)
