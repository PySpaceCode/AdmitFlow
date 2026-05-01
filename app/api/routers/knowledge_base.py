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

@router.get("/documents", summary="List all uploaded knowledge base documents")
def get_documents(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
) -> List[KnowledgeBaseDocumentResponse]:
    docs = db.query(KnowledgeBaseDocument).filter(KnowledgeBaseDocument.institute_id == institute_id).all()
    # Manual mapping to camelCase for the schema if needed, but the middleware wraps the response
    return docs

@router.post("/upload", summary="Upload a PDF/DOCX knowledge base document")
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
    
    try:
        from app.services.ai_analysis import ai_analysis_service
        extracted_data = await ai_analysis_service.analyze_document(file_path)
    except Exception as e:
        print(f"CRITICAL ERROR: Knowledge extraction failed for {file.filename}: {str(e)}")
        # Provide a complete empty structure so the frontend doesn't show "not found" for everything
        extracted_data = {
            "institute_name": "Analysis Failed",
            "institute_tagline": str(e),
            "status": "error",
            "contact": {"phone": None, "email": None, "website": None, "address": None, "branches": []},
            "courses": [],
            "modules": [],
            "learning_outcomes": [],
            "tools_technologies": [],
            "faqs": [],
            "error_detail": str(e)
        }
    
    import json
    # Check if document already exists to prevent duplicates
    existing_doc = db.query(KnowledgeBaseDocument).filter(
        KnowledgeBaseDocument.institute_id == institute_id,
        KnowledgeBaseDocument.file_name == file.filename
    ).first()

    if existing_doc:
        existing_doc.status = "processed"
        existing_doc.ai_report = json.dumps(extracted_data)
        db.commit()
        db.refresh(existing_doc)
        new_doc = existing_doc
    else:
        new_doc = KnowledgeBaseDocument(
            institute_id=institute_id,
            file_name=file.filename,
            file_url=f"/static/knowledge/{institute_id}_{file.filename}",
            status="processed",
            ai_report=json.dumps(extracted_data)
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
    
    return {
        "success": True,
        "message": "File uploaded and processed",
        "data": {
            "id": new_doc.id,
            "fileName": new_doc.file_name,
            "status": new_doc.status,
            "aiReport": new_doc.ai_report,
            "uploadedAt": new_doc.created_at.isoformat()
        }
    }

@router.post("/persona", summary="Save or update the AI agent persona")
def save_persona(
    persona_data: PersonaSchema,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    persona = db.query(Persona).filter(Persona.institute_id == institute_id).first()
    if not persona:
        persona = Persona(institute_id=institute_id)
        
    # Auto-generate persona description if not provided or to match user requirement
    desc = persona_data.persona_description
    if not desc:
        desc = (f"You are a {persona_data.tone_style.lower() if persona_data.tone_style else 'helpful'} "
                f"and enthusiastic {persona_data.designation if persona_data.designation else 'admissions counselor'} "
                f"representing the university. Your goal is to guide prospective students through the enrollment process "
                f"using a {persona_data.voice_gender.lower() if persona_data.voice_gender else 'friendly'} voice.")
    
    persona.agent_name = persona_data.agent_name
    persona.designation = persona_data.designation
    persona.tone_style = persona_data.tone_style
    persona.voice_gender = persona_data.voice_gender
    persona.voice_speed = persona_data.voice_speed
    persona.persona_description = desc
    
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

@router.post("/script", summary="Save or update the calling script")
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
