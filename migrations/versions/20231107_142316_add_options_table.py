"""Add options table

Revision ID: ad4b7cb3f1eb
Revises: 17b4741be087
Create Date: 2023-11-07 14:23:16.204597

"""

from typing import Sequence
from uuid import uuid4

import sqlalchemy as sa
import sqlalchemy.orm as saorm
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ad4b7cb3f1eb'
down_revision: str | None = '17b4741be087'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def get_session():
    # Create a session to use the ORM
    conn = op.get_bind()
    Session = saorm.sessionmaker()
    return Session(bind=conn)


def upgrade() -> None:
    # === Create options table ===
    op.create_table('options',
                    sa.Column('cutting_day', sa.SMALLINT(), server_default='1', nullable=False),
                    sa.Column('cutting_hour', postgresql.TIME(), server_default='00:00', nullable=False),
                    sa.Column('data_reconciliation_interval', sa.SMALLINT(), server_default='1', nullable=False),
                    sa.Column('data_reconciliation_hour', postgresql.TIME(), server_default='00:00', nullable=False),
                    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_index(op.f('ix_options_id'), 'options', ['id'], unique=False)

    from src.db.models.options import Options

    # Get a session
    session = get_session()

    # Create default departments
    options = [
        Options(id=uuid4(), cutting_day=1, cutting_hour="00:00",
                data_reconciliation_interval=1, data_reconciliation_hour="00:00"),
    ]

    # Insert data to the departments table
    session.add_all(options)
    session.commit()


def downgrade() -> None:
    op.drop_index(op.f('ix_options_id'), table_name='options')
    op.drop_table('options')
