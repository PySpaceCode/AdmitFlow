"""Add missing JSONB columns to settings and scripts

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-04-30

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # 1. Settings Table
    settings_columns = [col['name'] for col in inspector.get_columns('settings')]
    if 'config' not in settings_columns:
        op.add_column('settings', sa.Column('config', JSONB(), nullable=True))
        
    # 2. Scripts Table
    scripts_columns = [col['name'] for col in inspector.get_columns('scripts')]
    if 'sections' not in scripts_columns:
        op.add_column('scripts', sa.Column('sections', JSONB(), nullable=True))

def downgrade() -> None:
    op.drop_column('settings', 'config')
    op.drop_column('scripts', 'sections')
