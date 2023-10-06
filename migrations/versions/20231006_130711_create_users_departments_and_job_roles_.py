"""Create users, departments and job_roles tables

Revision ID: 914977b24c0c
Revises: 
Create Date: 2023-10-06 13:07:11.719063

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '914977b24c0c'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # === Create systemrole enum type ===
    sa.Enum('OTHER', 'WORKER', 'ADMIN', 'SUPPORT', name='systemrole').create(op.get_bind())  # type: ignore

    # === Create departments table ===
    op.create_table('departments',
                    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=False),
                    sa.Column('external_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_departments_id'), 'departments', ['id'], unique=False)

    # === Create job_roles table ===
    op.create_table('job_roles',
                    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=False),
                    sa.Column('department_id', sa.Uuid(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_job_roles_id'), 'job_roles', ['id'], unique=False)

    # === Create users table ===
    op.create_table('users',
                    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('email', sa.String(length=120), nullable=False),
                    sa.Column('password', sa.String(length=72), nullable=False),
                    sa.Column('names', sa.String(length=40), nullable=True),
                    sa.Column('lastnames', sa.String(length=40), nullable=True),
                    sa.Column('system_role',  # type: ignore
                              postgresql.ENUM('OTHER', 'WORKER', 'ADMIN', 'SUPPORT', name='systemrole', create_type=False), nullable=False),
                    sa.Column('job_role_id', sa.Uuid(), nullable=True),
                    sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['job_role_id'], ['job_roles.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_job_roles_id'), table_name='job_roles')
    op.drop_table('job_roles')
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_departments_id'), table_name='departments')
    op.drop_table('departments')
    op.drop_index(op.f('ix_clients_id'), table_name='clients')
    op.drop_table('clients')
    sa.Enum('OTHER', 'WORKER', 'ADMIN', 'SUPPORT', name='systemrole').drop(op.get_bind())  # type: ignore
