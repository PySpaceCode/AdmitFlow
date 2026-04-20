from typing import List, Optional
from datetime import datetime
from .base import BaseSchema

class CallTriggerRequest(BaseSchema):
    leadId: int

class CallTriggerResponse(BaseSchema):
    callId: int
    status: str

class MessageResponse(BaseSchema):
    speaker: str
    content: str

class ConversationActiveResponse(BaseSchema):
    id: int
    leadName: str
    aiPaused: bool
    lastMessage: Optional[str] = None

class ConversationThreadResponse(BaseSchema):
    messages: List[MessageResponse]

class ReplyRequest(BaseSchema):
    content: str

class ReplyResponse(BaseSchema):
    aiPaused: bool
