from app.db.session import Base

# Import all modules to ensure they are registered with Base
from . import user, institute, leads, bookings_settings, campaign, conversations, knowledge, script, calls, all_models

# Export Pyspace models for all_routes.py
from .all_models import (
    PyspaceOrganization as Organization,
    PyspaceAIAgent as AIAgent,
    PyspaceKnowledgeBase as KnowledgeBase,
    PyspaceIntent as Intent,
    PyspaceBehaviorRule as BehaviorRule,
    PyspaceCallFlow as CallFlow,
    PyspaceScript as Script,
    PyspacePromptLog as PromptLog,
    PyspaceLead as Lead,
    PyspaceConversation as Conversation,
    PyspaceBehaviorEvent as BehaviorEvent,
    PyspaceCall as Call,
    PyspaceFollowup as Followup,
)

# Export standard models
from .user import User
from .institute import Institute
from .bookings_settings import Settings, Booking
from .campaign import Campaign


