from typing import Optional


class Ticket(object):
    """Class to represent a ticket in SaragurosNet.

    Parameters:
    contenido (str): The content of the ticket
    asunto (str): The subject of the ticket
    departamento (str): The department of the ticket
    turno (str): The shift of the ticket
    fechavisita (str): The date of the ticket
    agendado (bool): If the ticket is scheduled or not
    """

    def __init__(self, contenido: str, asunto: str, departamento: str, turno: str, fechavisita: str, agendado: bool):
        self.id: Optional[int] = None
        self.id_cliente: Optional[str] = None

        self.contenido = contenido
        self.asunto = asunto
        self.departamento = departamento
        self.turno = turno
        self.fechavisita = fechavisita
        self.agendado = agendado

    def __str__(self):
        return f"Ticket({self.id}, {self.id_cliente}, {self.contenido}, {self.asunto}, {self.departamento}, {self.turno}, {self.fechavisita}, {self.agendado})"
