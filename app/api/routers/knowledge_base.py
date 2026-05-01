import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.knowledge import KnowledgeBaseDocument, Persona
from app.models.script import Script
from app.schemas.knowledge_base import PersonaSchema, ScriptSchema, KnowledgeBaseDocumentResponse
from app.services.ai_analysis import ai_analysis_service
import json

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

async def run_ai_analysis(doc_id: int, file_path: str, db: Session):
    try:
        report = await ai_analysis_service.analyze_document(file_path)
        
        doc = db.query(KnowledgeBaseDocument).filter(KnowledgeBaseDocument.id == doc_id).first()
        if doc:
            doc.ai_report = json.dumps(report)
            doc.status = "processed"
            db.commit()
    except Exception as e:
        print(f"Error in background analysis: {e}")
        doc = db.query(KnowledgeBaseDocument).filter(KnowledgeBaseDocument.id == doc_id).first()
        if doc:
            doc.status = "error"
            db.commit()

@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
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
    
    # Trigger AI analysis as a background task to not block the upload response
    # However, since the frontend expects the report immediately, we might want to do it synchronously
    # OR we can update the frontend to poll.
    # For now, let's try to do it synchronously if it's not too slow, or just return and let them poll.
    # Actually, the user wants to see the analysis. Let's do it synchronously for better "WOW" effect if it finishes quickly.
    
    try:
        report = await ai_analysis_service.analyze_document(file_path)
        new_doc.ai_report = json.dumps(report)
        new_doc.status = "processed"
        db.commit()
        db.refresh(new_doc)
    except Exception as e:
        print(f"Analysis failed during upload: {e}")
        # We'll leave it as "processing" or set to "error"
    
    return {
        "success": True,
        "message": "File uploaded and analyzed",
        "data": {
            "id": new_doc.id,
            "fileName": new_doc.file_name,
            "status": new_doc.status,
            "aiReport": new_doc.ai_report,
            "uploadedAt": new_doc.created_at.isoformat()
        }
    }

@router.patch("/documents/{doc_id}/report")
async def update_document_report(
    doc_id: int,
    report_data: dict,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    doc = db.query(KnowledgeBaseDocument).filter(
        KnowledgeBaseDocument.id == doc_id,
        KnowledgeBaseDocument.institute_id == institute_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc.ai_report = json.dumps(report_data)
    db.commit()
    
    return {
        "success": True,
        "message": "Knowledge updated successfully",
        "data": report_data
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
