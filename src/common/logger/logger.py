from src.common.logger.types import AlertType


class Logger:
    """Class to log messages in the console."""

    _instance = None

    _func_names_to_ignore = ["<module>", "__call__", "__new__"]
    _module_char_length = 40

    def __new__(cls, func_names_to_ignore: list[str] | None = None, module_char_length: int | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            if func_names_to_ignore:
                cls._instance._add_func_names_to_ignore(func_names_to_ignore)

            if module_char_length:
                cls._instance._set_module_char_length(module_char_length)

        return cls._instance

    @staticmethod
    def _set_module_char_length(module_char_length: int):
        """Set the length of the module name.

        Parameters:
        module_char_length (int): The length of the module name
        """

        Logger._module_char_length = module_char_length

    @staticmethod
    def _add_func_names_to_ignore(func_names: list[str]):
        """Add function names to ignore.

        Default function names to ignore:
        - <module>
        - __call__
        - __new__

        Parameters:
        func_names (list[str]): The function names to ignore
        """

        Logger._func_names_to_ignore.extend(func_names)

    @staticmethod
    def info(msg: str, caller_name: str | None = None):
        """Log an `information` message in the console.

        Parameters:
        msg (str): The message to log
        """

        Logger._log(AlertType.INFO, msg, caller_name)

    @staticmethod
    def error(msg: str, caller_name: str | None = None):
        """Log an `error` message in the console.

        Parameters:
        msg (str): The message to log
        """

        Logger._log(AlertType.ERROR, msg, caller_name)

    @staticmethod
    def warn(msg: str, caller_name: str | None = None):
        """Log a `warning` message in the console.

        Parameters:
        msg (str): The message to log
        """

        Logger._log(AlertType.WARNING, msg, caller_name)

    @staticmethod
    def alert(msg: str, caller_name: str | None = None):
        """Log an `alert` message in the console.

        Parameters:
        msg (str): The message to log
        """

        Logger._log(AlertType.ALERT, msg, caller_name)

    @staticmethod
    def debug(msg: str, caller_name: str | None = None):
        """Log a `debug` message in the console.

        Parameters:
        msg (str): The message to log
        """

        Logger._log(AlertType.DEBUG, msg, caller_name)

    @staticmethod
    def _log(alert_type: AlertType, msg: str, caller_name: str | None = None):
        """Log a message in the console.

        Parameters:
        alert_type (str): The type of the alert
        msg (str): The message to log
        """

        if not caller_name:
            import inspect
            caller_frame = inspect.stack()[2]
            caller_module = inspect.getmodule(caller_frame[0])
            caller_function_name = caller_frame[3]  # function name
            caller_module_name = caller_module.__name__ if caller_module else "UNKNOWN"

            if caller_function_name not in Logger._func_names_to_ignore:
                caller_module_name = f"{caller_module_name.split('.')[-1]}.{caller_function_name}"
        else:
            caller_module_name = caller_name

        print(f"[{alert_type:^5}][{caller_module_name:^{Logger._module_char_length}}]: {msg}")
