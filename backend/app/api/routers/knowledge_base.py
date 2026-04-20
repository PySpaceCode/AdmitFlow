import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.knowledge import KnowledgeBaseDocument, Persona
from app.models.script import Script
from app.schemas.knowledge_base import PersonaSchema, ScriptSchema, KnowledgeBaseDocumentResponse

router = APIRouter()

UPLOAD_DIR = "uploads/knowledge"

@router.get("/documents")
def get_documents(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
) -> List[KnowledgeBaseDocumentResponse]:
    docs = db.query(KnowledgeBaseDocument).filter(KnowledgeBaseDocument.institute_id == institute_id).all()
    # Manual mapping to camelCase for the schema if needed, but the middleware wraps the response
    return docs

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(..., alias="file"),
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, f"{institute_id}_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not save file")
    
    new_doc = KnowledgeBaseDocument(
        institute_id=institute_id,
        file_name=file.filename,
        file_url=f"/static/knowledge/{institute_id}_{file.filename}",
        status="processing",
        ai_report=None
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    return {
        "success": True,
        "message": "File uploaded",
        "data": {
            "id": new_doc.id,
            "fileName": new_doc.file_name,
            "status": new_doc.status,
            "uploadedAt": new_doc.created_at.isoformat()
        }
    }

@router.post("/persona")
def save_persona(
    persona_data: PersonaSchema,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    persona = db.query(Persona).filter(Persona.institute_id == institute_id).first()
    if not persona:
        persona = Persona(institute_id=institute_id)
    
    persona.agent_name = persona_data.agent_name
    persona.designation = persona_data.designation
    persona.tone_style = persona_data.tone_style
    persona.voice_gender = persona_data.voice_gender
    persona.voice_speed = persona_data.voice_speed
    persona.persona_description = persona_data.persona_description
    
    db.add(persona)
    db.commit()
    db.refresh(persona)
    
    return {
        "success": True,
        "message": "Persona saved",
        "data": {
            "id": persona.id,
            "agent_name": persona.agent_name,
            "designation": persona.designation,
            "tone_style": persona.tone_style,
            "voice_gender": persona.voice_gender,
            "voice_speed": persona.voice_speed,
            "persona_description": persona.persona_description
        }
    }

@router.post("/script")
def save_script(
    script_data: ScriptSchema,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    script = db.query(Script).filter(Script.institute_id == institute_id).first()
    if not script:
        script = Script(institute_id=institute_id)
    
    script.sections = script_data.sections # Save JSONB directly
    
    db.add(script)
    db.commit()
    db.refresh(script)
    
    return {
        "success": True,
        "message": "Script saved",
        "data": {
            "scriptId": script.id,
            "sections": script.sections
        }
    }
