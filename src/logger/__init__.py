class Logger:
    """Class to log messages in the console."""

    @staticmethod
    def info(msg: str):
        """Log an `information` message in the console.

        Parameters:
        msg (str): The message to log
        """

        Logger._log("INF", msg)

    @staticmethod
    def error(msg: str):
        """Log an `error` message in the console.

        Parameters:
        msg (str): The message to log
        """

        Logger._log("ERR", msg)

    @staticmethod
    def warn(msg: str):
        """Log a `warning` message in the console.

        Parameters:
        msg (str): The message to log
        """

        Logger._log("WAR", msg)

    @staticmethod
    def alert(msg: str):
        """Log an `alert` message in the console.

        Parameters:
        msg (str): The message to log
        """

        Logger._log("ALE", msg)

    @staticmethod
    def _log(alert_type: str, msg: str):
        """Log a message in the console.

        Parameters:
        alert_type (str): The type of the alert
        msg (str): The message to log
        """

        import inspect
        caller_frame = inspect.stack()[2]
        caller_module = inspect.getmodule(caller_frame[0])
        caller_name = caller_frame[3]  # function name
        caller_name = caller_module.__name__ if caller_module else "UNKNOWN"

        if caller_frame[3] != "<module>" and caller_frame[3] != "__call__" and caller_frame[3] != "__new__":
            caller_name = f"{caller_name}.{caller_frame[3]}"

        print(f"[{alert_type:^5}][{caller_name:^40}]: {msg}")


# Ejemplo de uso de la clase Logger
if __name__ == "__main__":
    Logger.info("This is an information message.")
    Logger.error("This is an error message.")
    Logger.warn("This is a warning message.")
    Logger.alert("This is an alert message.")

    def function_test():
        Logger.info("This is an information message.")
        Logger.error("This is an error message.")
        Logger.warn("This is a warning message.")
        Logger.alert("This is an alert message.")

    print("="*50)

    function_test()
