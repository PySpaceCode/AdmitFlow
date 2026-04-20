from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.calls import Call
from app.models.leads import Lead
from app.models.conversations import Conversation, Message
from app.schemas.calls_conv import (
    CallTriggerRequest, 
    CallTriggerResponse, 
    ConversationActiveResponse, 
    ConversationThreadResponse, 
    ReplyRequest, 
    ReplyResponse
)

router = APIRouter()

@router.post("/call/trigger")
def trigger_call(
    request_data: CallTriggerRequest,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    lead = db.query(Lead).filter(Lead.id == request_data.leadId, Lead.institute_id == institute_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    new_call = Call(
        institute_id=institute_id,
        lead_id=lead.id
    )
    db.add(new_call)
    
    # Update lead status
    lead.status = "contacting"
    
    db.commit()
    db.refresh(new_call)
    
    return {
        "success": True,
        "message": "Call started",
        "data": {
            "callId": new_call.id,
            "status": "in-progress"
        }
    }

@router.get("/conversations/active")
def get_active_conversations(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    convs = db.query(Conversation).filter(Conversation.institute_id == institute_id).all()
    
    data = []
    for conv in convs:
        last_msg = db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.created_at.desc()).first()
        data.append({
            "id": conv.id,
            "leadName": conv.lead.name if conv.lead else "Unknown",
            "aiPaused": conv.ai_paused,
            "lastMessage": last_msg.content if last_msg else None
        })
    return data

@router.get("/conversations/{conversation_id}/thread")
def get_conversation_thread(
    conversation_id: int,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.institute_id == institute_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
    
    return {
        "messages": [
            {"speaker": m.speaker, "content": m.content} for m in messages
        ]
    }

@router.post("/conversations/{conversation_id}/reply")
def reply_to_conversation(
    conversation_id: int,
    reply_data: ReplyRequest,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.institute_id == institute_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    # Add human message
    new_msg = Message(
        conversation_id=conv.id,
        speaker="human",
        content=reply_data.content
    )
    db.add(new_msg)
    
    # Usually replying manually pauses the AI
    conv.ai_paused = True
    db.add(conv)
    
    db.commit()
    
    return {
        "success": True,
        "message": "Reply sent",
        "data": {
            "aiPaused": conv.ai_paused
        }
    }
