from typing import Optional


class Ticket(object):
    """Class to represent a ticket in SaragurosNet."""

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
