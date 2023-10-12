"""Create clients table

Revision ID: d764f989e569
Revises: 914977b24c0c
Create Date: 2023-10-06 16:26:03.197870

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd764f989e569'
down_revision: str | None = '914977b24c0c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # === Create clients table ===
    op.create_table('clients',
                    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('ci', sa.String(length=13), nullable=True),
                    sa.Column('names', sa.String(length=40), nullable=True),
                    sa.Column('lastnames', sa.String(length=40), nullable=True),
                    sa.Column('phone', sa.String(length=13), nullable=False),
                    sa.Column('saraguros_id', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),

                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_clients_ci'), 'clients', ['ci'], unique=True)
    op.create_index(op.f('ix_clients_id'), 'clients', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_clients_id'), table_name='clients')
    op.drop_index(op.f('ix_clients_ci'), table_name='clients')
    op.drop_table('clients')
