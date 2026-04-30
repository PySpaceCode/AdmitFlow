"""Add missing columns to institutes table

Revision ID: a1b2c3d4e5f6
Revises: bdb88bddeaf4
Create Date: 2026-04-30

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'bdb88bddeaf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add columns that were added to the Institute model after the initial migration."""
    # Use batch_alter_table for compatibility, but since this is Postgres we can use op.add_column directly.
    # Each column is added only if it doesn't already exist (safe to re-run).

    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('institutes')]

    columns_to_add = {
        'email':              sa.Column('email',               sa.String(),  nullable=True),
        'phone':              sa.Column('phone',               sa.String(),  nullable=True),
        'institute_type':     sa.Column('institute_type',      sa.String(),  nullable=True),
        'city_address':       sa.Column('city_address',        sa.String(),  nullable=True),
        'website_url':        sa.Column('website_url',         sa.String(),  nullable=True),
        'email_verification': sa.Column('email_verification',  sa.String(),  nullable=True),
        'phone_verification': sa.Column('phone_verification',  sa.String(),  nullable=True),
        'social_fb':          sa.Column('social_fb',           sa.String(),  nullable=True),
        'social_ig':          sa.Column('social_ig',           sa.String(),  nullable=True),
        'social_linkedin':    sa.Column('social_linkedin',     sa.String(),  nullable=True),
        'social_x':           sa.Column('social_x',            sa.String(),  nullable=True),
    }

    for col_name, col_def in columns_to_add.items():
        if col_name not in existing_columns:
            op.add_column('institutes', col_def)


def downgrade() -> None:
    """Remove the columns added in this migration."""
    cols = [
        'email', 'phone', 'institute_type', 'city_address', 'website_url',
        'email_verification', 'phone_verification',
        'social_fb', 'social_ig', 'social_linkedin', 'social_x'
    ]
    for col in cols:
        op.drop_column('institutes', col)
