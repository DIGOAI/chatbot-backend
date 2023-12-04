"""Add massive_templates table

Revision ID: 4c76fc92002e
Revises: 17b4741be087
Create Date: 2023-11-08 12:13:34.723936

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4c76fc92002e'
down_revision: str | None = '17b4741be087'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # === Create massivetemplatetype enum type ===
    sa.Enum('EMAIL', 'SMS', 'WHATSAPP', name='massivetemplatetype').create(op.get_bind())  # type: ignore

    # === Create massive_templates table ===
    op.create_table('massive_templates',
                    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('type',  # type: ignore
                              postgresql.ENUM('EMAIL', 'SMS', 'WHATSAPP', name='massivetemplatetype', create_type=False), nullable=False),
                    sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_index(op.f('ix_massive_templates_id'), 'massive_templates', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_massive_templates_id'), table_name='massive_templates')
    op.drop_table('massive_templates')
    sa.Enum('EMAIL', 'SMS', 'WHATSAPP', name='massivetemplatetype').drop(op.get_bind())  # type: ignore
