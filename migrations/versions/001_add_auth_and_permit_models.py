"""Add auth and permit models

Revision ID: 001
Revises: 
Create Date: 2025-12-15 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update users table - add hashed_password and is_active columns
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.alter_column('users', 'role', existing_type=sa.String(), nullable=True, server_default='user')
    
    # Create permits table
    op.create_table('permits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_name', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('system_size_kw', sa.Numeric(), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default='pending'),
        sa.Column('pdf_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permits_id'), 'permits', ['id'], unique=False)
    
    # Update designs table - rename metadata to design_metadata
    op.alter_column('designs', 'metadata', new_column_name='design_metadata')


def downgrade() -> None:
    # Revert designs table change
    op.alter_column('designs', 'design_metadata', new_column_name='metadata')
    
    # Drop permits table
    op.drop_index(op.f('ix_permits_id'), table_name='permits')
    op.drop_table('permits')
    
    # Revert users table changes
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'hashed_password')
    op.alter_column('users', 'role', existing_type=sa.String(), nullable=True, server_default=None)
