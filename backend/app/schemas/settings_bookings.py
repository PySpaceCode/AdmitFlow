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

class BookingUpdateRequest(BaseSchema):
    status: str
    agentAssignedId: int

class SettingsSaveRequest(BaseSchema):
    whatsappEnabled: bool
    callEnabled: bool
