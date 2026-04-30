from typing import List, Optional
from datetime import datetime
from .base import BaseSchema

class LeadResponse(BaseSchema):
    id: int
    name: str
    phone: str
    email: Optional[str] = None
    course: Optional[str] = None
    status: str
    created_at: datetime

class CallingConfigurationRequest(BaseSchema):
    calling_days: List[str]
    calling_window_start: str
    calling_window_end: str
    maximum_daily_call_attempts: int
    human_agent_name: str
    human_agent_phone_number: str

class CampaignResponse(BaseSchema):
    campaignId: int
    status: str
