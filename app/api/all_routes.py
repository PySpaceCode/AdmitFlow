from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.models import (
    Organization, AIAgent, KnowledgeBase, Intent, BehaviorRule, 
    Script, PromptLog, Lead, Conversation, Call
)
from app.schemas.all_schemas import (
    AIAgentCreate, AIAgentResponse, KnowledgeBaseCreate, KnowledgeBaseResponse,
    IntentCreate, IntentResponse, BehaviorRuleCreate, BehaviorRuleResponse,
    ScriptCreate, ScriptResponse, LeadCreate, LeadResponse,
    ConversationCreate, ConversationResponse, CallCreate, CallResponse,
    AuthRegister, AuthLogin, AuthResponse
)

router = APIRouter()

# --- Auth Placeholder ---
# Auth endpoints have been moved to app.api.routers.auth

# --- Agents ---
@router.post("/agents", response_model=AIAgentResponse)
def create_agent(agent: AIAgentCreate, db: Session = Depends(get_db)):
    # Placeholder organization_id for now
    org = db.query(Organization).first()
    if not org:
        org = Organization(name="Default Org")
        db.add(org)
        db.commit()
        db.refresh(org)
    
    db_agent = AIAgent(**agent.dict(), organization_id=org.id)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.get("/agents/{id}", response_model=AIAgentResponse)
def get_agent(id: UUID, db: Session = Depends(get_db)):
    agent = db.query(AIAgent).filter(AIAgent.id == id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/agents/{id}", response_model=AIAgentResponse)
def update_agent(id: UUID, agent_update: AIAgentCreate, db: Session = Depends(get_db)):
    agent = db.query(AIAgent).filter(AIAgent.id == id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    for k, v in agent_update.dict(exclude_unset=True).items():
        setattr(agent, k, v)
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/agents/{id}")
def delete_agent(id: UUID, db: Session = Depends(get_db)):
    agent = db.query(AIAgent).filter(AIAgent.id == id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return {"message": "Agent deleted"}

# --- Knowledge Base ---
@router.post("/agents/{id}/knowledge", response_model=KnowledgeBaseResponse)
def add_knowledge(id: UUID, kb: KnowledgeBaseCreate, db: Session = Depends(get_db)):
    db_kb = KnowledgeBase(**kb.dict(), agent_id=id)
    db.add(db_kb)
    db.commit()
    db.refresh(db_kb)
    return db_kb

@router.get("/agents/{id}/knowledge", response_model=List[KnowledgeBaseResponse])
def get_knowledge(id: UUID, db: Session = Depends(get_db)):
    return db.query(KnowledgeBase).filter(KnowledgeBase.agent_id == id).all()

@router.put("/knowledge/{kb_id}", response_model=KnowledgeBaseResponse)
def update_knowledge(kb_id: UUID, kb_update: KnowledgeBaseCreate, db: Session = Depends(get_db)):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    for k, v in kb_update.dict(exclude_unset=True).items():
        setattr(kb, k, v)
    db.commit()
    db.refresh(kb)
    return kb

@router.delete("/knowledge/{kb_id}")
def delete_knowledge(kb_id: UUID, db: Session = Depends(get_db)):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    db.delete(kb)
    db.commit()
    return {"message": "Knowledge base deleted"}

# --- Intents ---
@router.post("/agents/{id}/intents", response_model=IntentResponse)
def create_intent(id: UUID, intent: IntentCreate, db: Session = Depends(get_db)):
    db_intent = Intent(**intent.dict(), agent_id=id)
    db.add(db_intent)
    db.commit()
    db.refresh(db_intent)
    return db_intent

@router.get("/agents/{id}/intents", response_model=List[IntentResponse])
def get_intents(id: UUID, db: Session = Depends(get_db)):
    return db.query(Intent).filter(Intent.agent_id == id).all()

@router.put("/intents/{intent_id}", response_model=IntentResponse)
def update_intent(intent_id: UUID, intent_update: IntentCreate, db: Session = Depends(get_db)):
    intent = db.query(Intent).filter(Intent.id == intent_id).first()
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    for k, v in intent_update.dict(exclude_unset=True).items():
        setattr(intent, k, v)
    db.commit()
    db.refresh(intent)
    return intent

@router.delete("/intents/{intent_id}")
def delete_intent(intent_id: UUID, db: Session = Depends(get_db)):
    intent = db.query(Intent).filter(Intent.id == intent_id).first()
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    db.delete(intent)
    db.commit()
    return {"message": "Intent deleted"}

# --- Behavior Rules ---
@router.post("/agents/{id}/rules", response_model=BehaviorRuleResponse)
def create_rule(id: UUID, rule: BehaviorRuleCreate, db: Session = Depends(get_db)):
    db_rule = BehaviorRule(**rule.dict(), agent_id=id)
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.get("/agents/{id}/rules", response_model=List[BehaviorRuleResponse])
def get_rules(id: UUID, db: Session = Depends(get_db)):
    return db.query(BehaviorRule).filter(BehaviorRule.agent_id == id).all()

@router.put("/rules/{rule_id}", response_model=BehaviorRuleResponse)
def update_rule(rule_id: UUID, rule_update: BehaviorRuleCreate, db: Session = Depends(get_db)):
    rule = db.query(BehaviorRule).filter(BehaviorRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    for k, v in rule_update.dict(exclude_unset=True).items():
        setattr(rule, k, v)
    db.commit()
    db.refresh(rule)
    return rule

@router.delete("/rules/{rule_id}")
def delete_rule(rule_id: UUID, db: Session = Depends(get_db)):
    rule = db.query(BehaviorRule).filter(BehaviorRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted"}

# --- Script ---
@router.post("/agents/{id}/script", response_model=ScriptResponse)
def create_script(id: UUID, script: ScriptCreate, db: Session = Depends(get_db)):
    db_script = Script(**script.dict(), agent_id=id)
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return db_script

@router.get("/agents/{id}/script", response_model=List[ScriptResponse])
def get_script(id: UUID, db: Session = Depends(get_db)):
    return db.query(Script).filter(Script.agent_id == id).all()

@router.put("/script/{script_id}", response_model=ScriptResponse)
def update_script(script_id: UUID, script_update: ScriptCreate, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    for k, v in script_update.dict(exclude_unset=True).items():
        setattr(script, k, v)
    db.commit()
    db.refresh(script)
    return script

@router.post("/script/{script_id}/approve", response_model=ScriptResponse)
def approve_script(script_id: UUID, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    script.status = "approved"
    db.commit()
    db.refresh(script)
    return script

# --- Prompt System (CORE) ---
@router.get("/agents/{id}/preview-prompt")
def preview_prompt(id: UUID, db: Session = Depends(get_db)):
    # Mocking prompt builder
    knowledge = db.query(KnowledgeBase).filter(KnowledgeBase.agent_id == id).all()
    intents = db.query(Intent).filter(Intent.agent_id == id).all()
    rules = db.query(BehaviorRule).filter(BehaviorRule.agent_id == id).all()
    script = db.query(Script).filter(Script.agent_id == id, Script.status == "approved").first()
    
    knowledge_str = "\\n".join([f"{k.title}: {k.content}" for k in knowledge])
    intents_str = "\\n".join([f"If user triggers {i.triggers} -> {i.response}" for i in intents])
    rules_str = "\\n".join([f"If {r.condition_type} == {r.condition_value} -> {r.action_type}" for r in rules])
    script_str = script.modified_script if script else "No approved script."

    prompt = f"""You are a human-like admission counselor.
    =====================
    KNOWLEDGE
    =====================
    {knowledge_str}
    =====================
    INTENTS
    =====================
    {intents_str}
    =====================
    CALL SCRIPT
    =====================
    {script_str}
    =====================
    RULES
    =====================
    {rules_str}
    =====================
    INSTRUCTIONS
    =====================
    - Be natural
    - Be concise
    - Sound human
    """
    return {"prompt": prompt}

@router.post("/agents/{id}/deploy")
def deploy_agent(id: UUID, db: Session = Depends(get_db)):
    # Mock deploy
    agent = db.query(AIAgent).filter(AIAgent.id == id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    prompt = preview_prompt(id, db)["prompt"]
    
    # Save prompt log
    prompt_log = PromptLog(agent_id=id, final_prompt=prompt, version=1)
    db.add(prompt_log)
    
    # Update agent
    agent.status = "active"
    agent.smallest_agent_id = "smallest-mock-id"
    
    db.commit()
    return {"message": "Agent deployed", "smallest_agent_id": agent.smallest_agent_id}

# --- Leads ---
@router.post("/leads", response_model=LeadResponse)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    org = db.query(Organization).first()
    if not org:
        org = Organization(name="Default Org")
        db.add(org)
        db.commit()
        db.refresh(org)

    db_lead = Lead(**lead.dict(), organization_id=org.id)
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.get("/leads", response_model=List[LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()

@router.put("/leads/{id}", response_model=LeadResponse)
def update_lead(id: UUID, lead_update: LeadCreate, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    for k, v in lead_update.dict(exclude_unset=True).items():
        setattr(lead, k, v)
    db.commit()
    db.refresh(lead)
    return lead

# --- Conversations ---
@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(lead_id: UUID, conv: ConversationCreate, db: Session = Depends(get_db)):
    db_conv = Conversation(**conv.dict(), lead_id=lead_id)
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv

@router.get("/leads/{id}/conversations", response_model=List[ConversationResponse])
def get_conversations(id: UUID, db: Session = Depends(get_db)):
    return db.query(Conversation).filter(Conversation.lead_id == id).all()

# --- Calls ---
@router.post("/calls/trigger")
def trigger_call(call_data: dict, db: Session = Depends(get_db)):
    # Trigger call logic placeholder
    lead_id = call_data.get("lead_id")
    agent_id = call_data.get("agent_id")
    if not lead_id or not agent_id:
        raise HTTPException(status_code=400, detail="Missing lead_id or agent_id")
    
    new_call = Call(lead_id=lead_id, agent_id=agent_id, call_status="triggered")
    db.add(new_call)
    db.commit()
    db.refresh(new_call)
    return {"message": "Call triggered", "call_id": new_call.id}

@router.post("/calls/webhook")
def call_webhook(webhook_data: dict, db: Session = Depends(get_db)):
    # Webhook placeholder
    return {"message": "Webhook received"}

