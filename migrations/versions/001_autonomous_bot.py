"""Add autonomous bot models and update user model

Revision ID: 001_autonomous_bot
Revises: 
Create Date: 2025-12-16 21:51:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_autonomous_bot'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Update users table - add authentication fields
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'))
    
    # Fix designs table - rename metadata column to avoid SQLAlchemy reserved word
    op.alter_column('designs', 'metadata', new_column_name='design_metadata')
    
    # Create bot_tasks table
    op.create_table('bot_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_type', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default='pending'),
        sa.Column('input_data', sa.JSON(), nullable=True),
        sa.Column('output_data', sa.JSON(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bot_tasks_id'), 'bot_tasks', ['id'], unique=False)
    
    # Create bot_workflows table
    op.create_table('bot_workflows',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('workflow_type', sa.String(), nullable=True),
        sa.Column('steps', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('success_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('failure_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bot_workflows_id'), 'bot_workflows', ['id'], unique=False)


def downgrade() -> None:
    # Drop bot tables
    op.drop_index(op.f('ix_bot_workflows_id'), table_name='bot_workflows')
    op.drop_table('bot_workflows')
    op.drop_index(op.f('ix_bot_tasks_id'), table_name='bot_tasks')
    op.drop_table('bot_tasks')
    
    # Revert designs table column rename
    op.alter_column('designs', 'design_metadata', new_column_name='metadata')
    
    # Remove columns from users table
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'hashed_password')
