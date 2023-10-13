"""Create messages table

Revision ID: 8038fc068412
Revises: 06fda5194c86
Create Date: 2023-10-07 11:59:57.813892

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8038fc068412'
down_revision: str | None = '06fda5194c86'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # === Create messagetype enum type ===
    sa.Enum('IN', 'OUT', name='messagetype').create(op.get_bind())  # type: ignore

    # === Create messages table ===
    op.create_table('messages',
                    sa.Column('id', sa.String(length=34), nullable=False),
                    sa.Column('sender', sa.String(length=13), nullable=False),
                    sa.Column('receiver', sa.String(length=13), nullable=False),
                    sa.Column('message', sa.Text(), nullable=True),
                    sa.Column('media_url', sa.Text(), nullable=True),
                    sa.Column('message_type',  # type: ignore
                              postgresql.ENUM('IN', 'OUT', name='messagetype', create_type=False), nullable=False),
                    sa.Column('conversation_id', sa.Uuid(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),

                    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')

    sa.Enum('IN', 'OUT', name='messagetype').drop(op.get_bind())  # type: ignore
