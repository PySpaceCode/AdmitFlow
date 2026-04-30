from typing import Optional, List
from .base import BaseSchema

from enum import Enum

class InstituteTypeEnum(str, Enum):
    ENGINEERING_COLLEGE = "Engineering College"
    MEDICAL_COLLEGE = "Medical College"
    ARTS_SCIENCE_COLLEGE = "Arts & Science College"
    MBA_MANAGEMENT_INSTITUTE = "MBA / Management Institute"
    COACHING_CENTRE = "Coaching Centre"
    SCHOOL_K12 = "School (K-12)"
    POLYTECHNIC_VOCATIONAL = "Polytechnic / Vocational"
    UNIVERSITY = "University"
    OTHER = "Other"

class SocialMediaLinks(BaseSchema):
    fb: Optional[str] = None
    ig: Optional[str] = None
    linkedin: Optional[str] = None
    x: Optional[str] = None

class OnboardingStatusResponse(BaseSchema):
    onboarding_status: bool
    progress: Optional[int] = 0

class OnboardingSetupRequest(BaseSchema):
    fullName: str
    email: str
    instituteName: str
    instituteType: Optional[InstituteTypeEnum] = None
    cityAddress: Optional[str] = None
    websiteUrl: Optional[str] = None
    phone: Optional[str] = None
    emailVerification: Optional[str] = None
    phoneVerification: Optional[str] = None
    socialMediaLinks: Optional[SocialMediaLinks] = None

class KnowledgeBaseFileSchema(BaseSchema):
    id: int
    file_name: str
    status: str

class PersonaSchema(BaseSchema):
    agent_name: str
    designation: str
    tone_style: str
    voice_gender: str
    voice_speed: float
    persona_description: Optional[str] = None

class ScriptSectionSchema(BaseSchema):
    title: str
    content: str
    is_active: bool

class ScriptSchema(BaseSchema):
    sections: List[ScriptSectionSchema]
