from src.db.models.base import Base
from src.db.models.client import Client
from src.db.models.conversation import Conversation
from src.db.models.department import Department
from src.db.models.massive_template import MassiveTemplate
from src.db.models.message import Message
from src.db.models.options import Options
from src.db.models.ticket import Ticket
from src.db.models.user import User

__all__ = [
    "Base",
    "Client",
    "Conversation",
    "Department",
    "MassiveTemplate",
    "Message",
    "Options",
    "Ticket",
    "User",
]
