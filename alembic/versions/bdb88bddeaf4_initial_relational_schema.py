"""Initial relational schema

Revision ID: bdb88bddeaf4
Revises: 
Create Date: 2026-04-17 22:25:16.258531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdb88bddeaf4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    # 1. Institutes
    if 'institutes' not in existing_tables:
        op.create_table('institutes',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('onboarding_status', sa.Boolean(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_institutes_id'), 'institutes', ['id'], unique=False)

    # 2. Campaigns
    if 'campaigns' not in existing_tables:
        op.create_table('campaigns',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('institute_id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('calling_days', sa.JSON(), nullable=False),
            sa.Column('time_start', sa.String(), nullable=False),
            sa.Column('time_end', sa.String(), nullable=False),
            sa.Column('max_attempts', sa.Integer(), nullable=True),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['institute_id'], ['institutes.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_campaigns_id'), 'campaigns', ['id'], unique=False)
        op.create_index(op.f('ix_campaigns_institute_id'), 'campaigns', ['institute_id'], unique=False)

    # 3. Knowledge Base Files
    if 'knowledge_base_files' not in existing_tables:
        op.create_table('knowledge_base_files',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('institute_id', sa.Integer(), nullable=False),
            sa.Column('file_name', sa.String(), nullable=False),
            sa.Column('file_url', sa.String(), nullable=False),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['institute_id'], ['institutes.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_knowledge_base_files_id'), 'knowledge_base_files', ['id'], unique=False)
        op.create_index(op.f('ix_knowledge_base_files_institute_id'), 'knowledge_base_files', ['institute_id'], unique=False)

    # 4. Leads
    if 'leads' not in existing_tables:
        op.create_table('leads',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('institute_id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('phone', sa.String(), nullable=False),
            sa.Column('email', sa.String(), nullable=True),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['institute_id'], ['institutes.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_leads_id'), 'leads', ['id'], unique=False)
        op.create_index(op.f('ix_leads_institute_id'), 'leads', ['institute_id'], unique=False)

    # 5. Personas
    if 'personas' not in existing_tables:
        op.create_table('personas',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('institute_id', sa.Integer(), nullable=False),
            sa.Column('agent_name', sa.String(), nullable=False),
            sa.Column('designation', sa.String(), nullable=False),
            sa.Column('tone_style', sa.String(), nullable=False),
            sa.Column('voice_gender', sa.String(), nullable=False),
            sa.Column('voice_speed', sa.Float(), nullable=True),
            sa.Column('persona_description', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['institute_id'], ['institutes.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_personas_id'), 'personas', ['id'], unique=False)
        op.create_index(op.f('ix_personas_institute_id'), 'personas', ['institute_id'], unique=False)

    # 6. Scripts
    if 'scripts' not in existing_tables:
        op.create_table('scripts',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('institute_id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['institute_id'], ['institutes.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_scripts_id'), 'scripts', ['id'], unique=False)
        op.create_index(op.f('ix_scripts_institute_id'), 'scripts', ['institute_id'], unique=False)

    # 7. Settings
    if 'settings' not in existing_tables:
        op.create_table('settings',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('institute_id', sa.Integer(), nullable=False),
            sa.Column('whatsapp_enabled', sa.Boolean(), nullable=True),
            sa.Column('call_enabled', sa.Boolean(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['institute_id'], ['institutes.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_settings_id'), 'settings', ['id'], unique=False)
        op.create_index(op.f('ix_settings_institute_id'), 'settings', ['institute_id'], unique=False)

    # 8. Users
    if 'users' not in existing_tables:
        op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('institute_id', sa.Integer(), nullable=False),
            sa.Column('full_name', sa.String(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password_hash', sa.String(), nullable=False),
            sa.Column('role', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['institute_id'], ['institutes.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
        op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
        op.create_index(op.f('ix_users_institute_id'), 'users', ['institute_id'], unique=False)

    # 9. Bookings
    if 'bookings' not in existing_tables:
        op.create_table('bookings',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('lead_id', sa.Integer(), nullable=False),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('agent_assigned_id', sa.Integer(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['agent_assigned_id'], ['users.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_bookings_id'), 'bookings', ['id'], unique=False)
        op.create_index(op.f('ix_bookings_lead_id'), 'bookings', ['lead_id'], unique=False)

    # 10. Calls
    if 'calls' not in existing_tables:
        op.create_table('calls',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('lead_id', sa.Integer(), nullable=False),
            sa.Column('campaign_id', sa.Integer(), nullable=True),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('duration', sa.Integer(), nullable=True),
            sa.Column('sentiment', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_calls_id'), 'calls', ['id'], unique=False)
        op.create_index(op.f('ix_calls_lead_id'), 'calls', ['lead_id'], unique=False)

    # 11. Conversations
    if 'conversations' not in existing_tables:
        op.create_table('conversations',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('lead_id', sa.Integer(), nullable=False),
            sa.Column('ai_paused', sa.Boolean(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_conversations_id'), 'conversations', ['id'], unique=False)
        op.create_index(op.f('ix_conversations_lead_id'), 'conversations', ['lead_id'], unique=False)

    # 12. Script Sections
    if 'script_sections' not in existing_tables:
        op.create_table('script_sections',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('script_id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('is_active', sa.Boolean(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['script_id'], ['scripts.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_script_sections_id'), 'script_sections', ['id'], unique=False)
        op.create_index(op.f('ix_script_sections_script_id'), 'script_sections', ['script_id'], unique=False)

    # 13. Messages
    if 'messages' not in existing_tables:
        op.create_table('messages',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('conversation_id', sa.Integer(), nullable=False),
            sa.Column('speaker', sa.String(), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)
        op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_conversation_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_script_sections_script_id'), table_name='script_sections')
    op.drop_index(op.f('ix_script_sections_id'), table_name='script_sections')
    op.drop_table('script_sections')
    op.drop_index(op.f('ix_conversations_lead_id'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_id'), table_name='conversations')
    op.drop_table('conversations')
    op.drop_index(op.f('ix_calls_lead_id'), table_name='calls')
    op.drop_index(op.f('ix_calls_id'), table_name='calls')
    op.drop_table('calls')
    op.drop_index(op.f('ix_bookings_lead_id'), table_name='bookings')
    op.drop_index(op.f('ix_bookings_id'), table_name='bookings')
    op.drop_table('bookings')
    op.drop_index(op.f('ix_users_institute_id'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_settings_institute_id'), table_name='settings')
    op.drop_index(op.f('ix_settings_id'), table_name='settings')
    op.drop_table('settings')
    op.drop_index(op.f('ix_scripts_institute_id'), table_name='scripts')
    op.drop_index(op.f('ix_scripts_id'), table_name='scripts')
    op.drop_table('scripts')
    op.drop_index(op.f('ix_personas_institute_id'), table_name='personas')
    op.drop_index(op.f('ix_personas_id'), table_name='personas')
    op.drop_table('personas')
    op.drop_index(op.f('ix_leads_institute_id'), table_name='leads')
    op.drop_index(op.f('ix_leads_id'), table_name='leads')
    op.drop_table('leads')
    op.drop_index(op.f('ix_knowledge_base_files_institute_id'), table_name='knowledge_base_files')
    op.drop_index(op.f('ix_knowledge_base_files_id'), table_name='knowledge_base_files')
    op.drop_table('knowledge_base_files')
    op.drop_index(op.f('ix_campaigns_institute_id'), table_name='campaigns')
    op.drop_index(op.f('ix_campaigns_id'), table_name='campaigns')
    op.drop_table('campaigns')
    op.drop_index(op.f('ix_institutes_id'), table_name='institutes')
    op.drop_table('institutes')

    # ### end Alembic commands ###
