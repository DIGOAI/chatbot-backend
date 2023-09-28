from src.db.database import Session
from src.db.database import engine as _engine
from src.db.db_connnection import DbConnection
from src.db.models import Base
from src.db.postgres import PostgreSQLConnection

__all__ = [
    'Base',
    'Session',
    'DbConnection',
    'PostgreSQLConnection',
    'setup_db'
]


def setup_db():
    Base.metadata.create_all(bind=_engine)
