from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from uuid import UUID
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class AIAgentBase(BaseModel):
    name: str
    status: Optional[str] = "draft"
    smallest_agent_id: Optional[str] = None
    tone: Optional[str] = None
    language: Optional[str] = None

class AIAgentCreate(AIAgentBase):
    pass

class AIAgentResponse(AIAgentBase):
    id: UUID
    organization_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class KnowledgeBaseBase(BaseModel):
    type: str
    title: str
    content: Dict[str, Any]

class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass

class KnowledgeBaseResponse(KnowledgeBaseBase):
    id: UUID
    agent_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class IntentBase(BaseModel):
    name: str
    triggers: Dict[str, Any]
    response: Optional[str] = None
    goal: Optional[str] = None
    tone: Optional[str] = None

class IntentCreate(IntentBase):
    pass

class IntentResponse(IntentBase):
    id: UUID
    agent_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class BehaviorRuleBase(BaseModel):
    condition_type: str
    condition_value: str
    action_type: str
    action_config: Dict[str, Any]
    priority: Optional[int] = 0

class BehaviorRuleCreate(BehaviorRuleBase):
    pass

class BehaviorRuleResponse(BehaviorRuleBase):
    id: UUID
    agent_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class CallFlowBase(BaseModel):
    opening: Optional[str] = None
    closing: Optional[str] = None
    steps: Optional[Dict[str, Any]] = None

class CallFlowCreate(CallFlowBase):
    pass

class CallFlowResponse(CallFlowBase):
    id: UUID
    agent_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class ScriptBase(BaseModel):
    generated_script: Optional[str] = None
    modified_script: Optional[str] = None
    status: Optional[str] = "draft"
    additional_instructions: Optional[str] = None

class ScriptCreate(ScriptBase):
    pass

class ScriptResponse(ScriptBase):
    id: UUID
    agent_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class LeadBase(BaseModel):
    name: str
    phone: str
    status: Optional[str] = None
    score: Optional[float] = 0.0
    decision_state: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: UUID
    organization_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    message: str
    sender: str
    channel: str
    intent_detected: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: UUID
    lead_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class CallBase(BaseModel):
    call_status: Optional[str] = None
    duration: Optional[int] = None
    transcript: Optional[str] = None

class CallCreate(CallBase):
    pass

class CallResponse(CallBase):
    id: UUID
    lead_id: UUID
    agent_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class AuthRegister(BaseModel):
    organization_name: str
    email: str
    password: str

class AuthLogin(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str
    organization_id: UUID

class CallTrigger(BaseModel):
    lead_id: UUID
    agent_id: UUID
