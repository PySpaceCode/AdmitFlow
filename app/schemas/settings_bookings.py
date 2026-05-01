from typing import Optional
from datetime import datetime
from .base import BaseSchema
from pydantic import BaseModel

class BookingResponse(BaseSchema):
    id: int
    lead_id: int
    status: str
    agent_assigned_id: Optional[int] = None
    created_at: datetime

class BookingWithLead(BaseSchema):
    id: int
    status: str
    scheduled_at: Optional[datetime] = None
    created_at: datetime
    lead_name: str
    lead_phone: str
    lead_course: Optional[str] = None
    agent_name: Optional[str] = None

class BookingUpdateRequest(BaseSchema):
    status: str
    agentAssignedId: int

class BookingRescheduleRequest(BaseSchema):
    scheduledAt: datetime

class SettingsSaveRequest(BaseSchema):
    whatsappEnabled: bool
    callEnabled: bool
