from src.api.db.models.base import Base
from src.api.db.models.client import Client
from src.api.db.models.conversation import Conversation
from src.api.db.models.department import Department
from src.api.db.models.job_role import JobRole
from src.api.db.models.message import Message
from src.api.db.models.user import User

__all__ = [
    "Base",
    "Client",
    "Conversation",
    "Department",
    "JobRole",
    "Message",
    "User",
]
