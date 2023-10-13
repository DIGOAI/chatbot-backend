"""Create conversations table

Revision ID: 06fda5194c86
Revises: d764f989e569
Create Date: 2023-10-06 16:27:52.964028

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '06fda5194c86'
down_revision: str | None = 'd764f989e569'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # === Create conversationstatus enum type ===
    sa.Enum('OPENED', 'CLOSED', name='conversationstatus').create(op.get_bind())  # type: ignore

    # === Create conversations table ===
    op.create_table('conversations',
                    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('client_phone', sa.String(length=13), nullable=False),
                    sa.Column('assistant_phone', sa.String(length=13), nullable=False),
                    sa.Column('client_id', sa.Uuid(), nullable=True),
                    sa.Column('status',  # type: ignore
                              postgresql.ENUM('OPENED', 'CLOSED', name='conversationstatus', create_type=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),

                    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_conversations_id'), 'conversations', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_conversations_id'), table_name='conversations')
    op.drop_table('conversations')

    sa.Enum('OPENED', 'CLOSED', name='conversationstatus').drop(op.get_bind())  # type: ignore
