from enum import Enum

from colorama import Back, Fore, Style, init


class AlertType(str, Enum):
    """Enum for the alert types."""

    INFO = "INF"
    ERROR = "ERR"
    WARNING = "WAR"
    ALERT = "ALE"
    DEBUG = "DEB"

    def __str__(self) -> str:
        return self.value


ColorDict = dict[AlertType, str]

COLORS: ColorDict = {
    AlertType.INFO: Back.BLUE + Fore.WHITE + Style.BRIGHT,
    AlertType.ERROR: Back.RED + Fore.WHITE + Style.BRIGHT,
    AlertType.WARNING: Back.YELLOW + Fore.BLACK + Style.BRIGHT,
    AlertType.ALERT: Back.GREEN + Fore.WHITE + Style.BRIGHT,
    AlertType.DEBUG: Back.MAGENTA + Fore.WHITE + Style.BRIGHT,
}


class Logger:
    """Class to log messages in the console."""

    func_names_to_ignore = ["<module>", "__call__", "__new__"]
    module_char_length = 40

    @staticmethod
    def add_func_names_to_ignore(func_names: list[str]):
        """Add function names to ignore.

        Default function names to ignore:
        - <module>
        - __call__
        - __new__

        Parameters:
        func_names (list[str]): The function names to ignore
        """

        Logger.func_names_to_ignore.extend(func_names)

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

            if caller_function_name not in Logger.func_names_to_ignore:
                # caller_module_name = f"{caller_module_name}.{caller_function_name}"
                caller_module_name = f"{caller_module_name.split('.')[-1]}.{caller_function_name}"
        else:
            caller_module_name = caller_name

        init()

        try:
            print(f"{COLORS[alert_type]}[{alert_type:^5}]{Style.RESET_ALL}{Style.BRIGHT}[{caller_module_name:^{Logger.module_char_length}}]:{Style.RESET_ALL} {msg}")
        except Exception:
            print(f"{alert_type}[{alert_type:^5}][{caller_module_name:^{Logger.module_char_length}}]: {msg}")
