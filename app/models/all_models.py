import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class PyspaceOrganization(Base):
    __tablename__ = 'pyspace_organizations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    agents = relationship("PyspaceAIAgent", back_populates="organization")
    leads = relationship("PyspaceLead", back_populates="organization")

class PyspaceAIAgent(Base):
    __tablename__ = 'pyspace_ai_agents'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_organizations.id'), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="draft") # draft / active
    smallest_agent_id = Column(String, nullable=True)
    tone = Column(String, nullable=True)
    language = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organization = relationship("PyspaceOrganization", back_populates="agents")
    knowledge_base = relationship("PyspaceKnowledgeBase", back_populates="agent")
    intents = relationship("PyspaceIntent", back_populates="agent")
    behavior_rules = relationship("PyspaceBehaviorRule", back_populates="agent")
    call_flows = relationship("PyspaceCallFlow", back_populates="agent")
    scripts = relationship("PyspaceScript", back_populates="agent")
    prompt_logs = relationship("PyspacePromptLog", back_populates="agent")

class PyspaceKnowledgeBase(Base):
    __tablename__ = 'pyspace_knowledge_base'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_ai_agents.id'), nullable=False)
    type = Column(String, nullable=False) # course / faq / general
    title = Column(String, nullable=False)
    content = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    agent = relationship("PyspaceAIAgent", back_populates="knowledge_base")

class PyspaceIntent(Base):
    __tablename__ = 'pyspace_intents'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_ai_agents.id'), nullable=False)
    name = Column(String, nullable=False)
    triggers = Column(JSONB, nullable=False)
    response = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    tone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agent = relationship("PyspaceAIAgent", back_populates="intents")

class PyspaceBehaviorRule(Base):
    __tablename__ = 'pyspace_behavior_rules'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_ai_agents.id'), nullable=False)
    condition_type = Column(String, nullable=False)
    condition_value = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    action_config = Column(JSONB, nullable=False)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agent = relationship("PyspaceAIAgent", back_populates="behavior_rules")

class PyspaceCallFlow(Base):
    __tablename__ = 'pyspace_call_flows'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_ai_agents.id'), nullable=False)
    opening = Column(String, nullable=True)
    closing = Column(String, nullable=True)
    steps = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agent = relationship("PyspaceAIAgent", back_populates="call_flows")

class PyspaceScript(Base):
    __tablename__ = 'pyspace_scripts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_ai_agents.id'), nullable=False)
    generated_script = Column(String, nullable=True)
    modified_script = Column(String, nullable=True)
    status = Column(String, default="draft") # draft / approved
    additional_instructions = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agent = relationship("PyspaceAIAgent", back_populates="scripts")

class PyspacePromptLog(Base):
    __tablename__ = 'prompt_logs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_ai_agents.id'), nullable=False)
    final_prompt = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agent = relationship("PyspaceAIAgent", back_populates="prompt_logs")

class PyspaceLead(Base):
    __tablename__ = 'pyspace_leads'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_organizations.id'), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    status = Column(String, nullable=True)
    score = Column(Float, default=0.0)
    decision_state = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organization = relationship("PyspaceOrganization", back_populates="leads")
    conversations = relationship("PyspaceConversation", back_populates="lead")
    behavior_events = relationship("PyspaceBehaviorEvent", back_populates="lead")
    calls = relationship("PyspaceCall", back_populates="lead")
    followups = relationship("PyspaceFollowup", back_populates="lead")

class PyspaceConversation(Base):
    __tablename__ = 'pyspace_conversations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_leads.id'), nullable=False)
    message = Column(String, nullable=False)
    sender = Column(String, nullable=False) # user / ai
    channel = Column(String, nullable=False) # whatsapp / chat
    intent_detected = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("PyspaceLead", back_populates="conversations")

class PyspaceBehaviorEvent(Base):
    __tablename__ = 'pyspace_behavior_events'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_leads.id'), nullable=False)
    event_type = Column(String, nullable=False)
    value = Column(String, nullable=True)
    score_impact = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("PyspaceLead", back_populates="behavior_events")

class PyspaceCall(Base):
    __tablename__ = 'pyspace_calls'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_leads.id'), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_ai_agents.id'), nullable=False)
    call_status = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    transcript = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("PyspaceLead", back_populates="calls")
    agent = relationship("PyspaceAIAgent")

class PyspaceFollowup(Base):
    __tablename__ = 'pyspace_followups'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey('pyspace_leads.id'), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    channel = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("PyspaceLead", back_populates="followups")

