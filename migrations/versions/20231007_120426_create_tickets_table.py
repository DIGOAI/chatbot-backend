"""Create tickets table

Revision ID: 0424e1a7b66b
Revises: 8038fc068412
Create Date: 2023-10-07 12:04:26.739803

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0424e1a7b66b'
down_revision: str | None = '8038fc068412'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # === Create ticketstatus enum type ===
    sa.Enum('WAITING', 'ATTENDING', 'CLOSED', 'UNSOLVED', name='ticketstatus').create(op.get_bind())  # type: ignore

    # === Create tickets table ===
    op.create_table('tickets',
                    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('external_id', sa.Integer(), nullable=True),
                    sa.Column('subject', sa.String(length=255), nullable=False),
                    sa.Column('shift', sa.String(length=13), nullable=True),
                    sa.Column('department_id', sa.Uuid(), nullable=False),
                    sa.Column('status',  # type: ignore
                              postgresql.ENUM('WAITING', 'ATTENDING', 'CLOSED', 'UNSOLVED', name='ticketstatus', create_type=False), nullable=False),
                    sa.Column('client_id', sa.Uuid(), nullable=False),
                    sa.Column('conversation_id', sa.Uuid(), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),

                    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_index(op.f('ix_tickets_id'), 'tickets', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_tickets_id'), table_name='tickets')
    op.drop_table('tickets')

    sa.Enum('WAITING', 'ATTENDING', 'CLOSED', 'UNSOLVED', name='ticketstatus').drop(op.get_bind())  # type: ignore
