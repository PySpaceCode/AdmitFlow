from typing import List, Optional
from datetime import datetime
from .base import BaseSchema

class KnowledgeBaseDocumentResponse(BaseSchema):
    id: int
    file_name: str
    status: str
    created_at: datetime

class PersonaSchema(BaseSchema):
    agent_name: str
    designation: str
    tone_style: str
    voice_gender: str
    voice_speed: float
    persona_description: Optional[str] = None

class ScriptSchema(BaseSchema):
    sections: List[dict] # Use dict to allow flexible section structure as seen in testing.json
