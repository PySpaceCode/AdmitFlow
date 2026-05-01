from typing import Optional, List
from .base import BaseSchema

class OnboardingStatusResponse(BaseSchema):
    onboarding_status: bool
    progress: Optional[int] = 0

class OnboardingSetupRequest(BaseSchema):
    fullName: str
    email: str
    instituteName: str

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
