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

class CampaignLaunchRequest(BaseSchema):
    callingDays: List[str]
    timeStart: str
    timeEnd: str
    maxAttempts: int
    fallbackName: str
    fallbackPhone: str

class CampaignResponse(BaseSchema):
    campaignId: int
    status: str
