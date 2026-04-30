from typing import List, Optional
from datetime import datetime
from .base import BaseSchema

# --- Calls ---
class CallResponse(BaseSchema):
    id: int
    lead_name: str
    phone: str
    sentiment: Optional[str]
    duration: Optional[int]
    created_at: datetime

class CallInitiateRequest(BaseSchema):
    lead_id: int

# --- Conversations ---
class MessageResponse(BaseSchema):
    sender_type: str
    content: str
    created_at: datetime

class ConversationResponse(BaseSchema):
    id: int
    lead_name: str
    ai_paused: bool
    status: str
    messages: List[MessageResponse]

# --- Bookings ---
class BookingResponse(BaseSchema):
    id: int
    lead_name: str
    datetime: datetime
    status: str
    agent_name: Optional[str]

class BookingUpdateStatus(BaseSchema):
    status: str
    agent_assigned_id: Optional[int] = None

# --- Settings ---
class SettingsResponse(BaseSchema):
    whatsapp_enabled: bool
    call_enabled: bool
