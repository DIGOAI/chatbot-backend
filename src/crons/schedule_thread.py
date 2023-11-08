import threading
import time

import schedule


class ScheduleThread(threading.Thread):
    """ Clase para ejecutar trabajos programados en segundo plano."""

    def __init__(self, event: threading.Event, interval: int = 1) -> None:
        """ Inicializa la clase ScheduleThread.

        Attributes:
        event (threading.Event): Evento que se puede establecer para detener la ejecución continua.
        interval (int): Intervalo de tiempo en segundos para verificar si hay trabajos pendientes. El valor predeterminado es 1.
        """
        self._cease_continuous_run = event
        self._interval = interval
        super().__init__()

    def run(self) -> None:
        while not self._cease_continuous_run.is_set():
            schedule.run_pending()
            seconds_to_next_execution = schedule.idle_seconds()
            time.sleep(seconds_to_next_execution or self._interval)


def run_schedules_continuously(interval: int = 1):
    """ Ejecuta los trabajos programados continuamente en segundo plano.
    Continuamente ejecuta, mientras se ejecutan trabajos pendientes en cada intervalo de tiempo transcurrido.

    Tenga en cuenta que es un comportamiento intencional que run_schedules_continuously() no ejecute trabajos perdidos.
    Por ejemplo, si ha registrado un trabajo que debe ejecutarse cada minuto y establece un intervalo de ejecución 
    continua de una hora, su trabajo no se ejecutará 60 veces en cada intervalo, sino solo una vez.

    Attributes:
    interval (int): Intervalo de tiempo en segundos para verificar si hay trabajos pendientes. El valor predeterminado es 1.

    Returns: threading. Evento que se puede establecer para detener la ejecución continua.
    """

    cease_continuous_run = threading.Event()

    continuous_thread = ScheduleThread(cease_continuous_run)
    continuous_thread.start()
    return cease_continuous_run


# class ScheduleManager:
#     _instance: "ScheduleManager" | None = None

#     def __new__(cls) -> "ScheduleManager":
#         if cls._instance is None:
#             cls._instance = super(ScheduleManager, cls).__new__(cls)
#             cls._instance._cease_continuous_run: threading.Event = threading.Event()
#             cls._instance._interval: int = 1
#             cls._instance._continuous_thread: "ScheduleManager.ScheduleThread" = cls._instance.ScheduleThread()

#         return cls._instance

#     def run_schedules_continuously(self, interval: int = 1) -> None:
#         self._instance._interval = interval
#         self._instance._continuous_thread.start()

#     def get_cease_continuous_run(self) -> threading.Event:
#         return self._instance._cease_continuous_run

#     class ScheduleThread(threading.Thread):
#         def run(self) -> None:
#             while not ScheduleManager._instance._cease_continuous_run.is_set():
#                 schedule.run_pending()
#                 seconds_to_next_execution = schedule.idle_seconds()
#                 time.sleep(seconds_to_next_execution or ScheduleManager._instance._interval)


# # Uso:
# manager: ScheduleManager = ScheduleManager()
# manager.run_schedules_continuously()

# # Para acceder al atributo cease_continuous_run desde cualquier parte del código:
# cease_continuous_run: threading.Event = manager.get_cease_continuous_run()
