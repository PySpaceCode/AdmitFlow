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
    
    # Strict JSON Extraction Structure for 10+ Modules & High Conversion
    mock_extracted_data = {
      "institute_name": "AdmissionFlow Academy",
      "institute_tagline": "Empowering Future Leaders",
      "contact": {
        "phone": "+91 9876543210",
        "email": "info@admissionflow.com",
        "website": "www.admissionflow.com",
        "address": "123 Education Hub, New Delhi",
        "branches": ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune"]
      },
      "courses": [
        {
          "course_name": "Full Stack Data Science & AI Mastery",
          "course_code": "DS-AI-2024",
          "eligibility": "B.Tech / BCA / BSc IT / Any Graduate with Math",
          "duration": "12 Months",
          "total_hours": "400+ Hours",
          "fee": "1,25,000",
          "fee_note": "Early bird discount of 10% available. EMI starts at ₹8,500/month.",
          "mode": "Hybrid (Live Online + In-person Workshops)",
          "coordinator": "Dr. Vikas Tiwari",
          "partner_institute": "Global Tech University"
        }
      ],
      "modules": [
        {"module_number": 1, "module_title": "Python for Data Science", "topics": ["Variables", "Loops", "Pandas", "NumPy", "Matplotlib", "Seaborn"]},
        {"module_number": 2, "module_title": "Mathematical Foundations", "topics": ["Linear Algebra", "Calculus", "Probability", "Statistics", "Hypothesis Testing"]},
        {"module_number": 3, "module_title": "Machine Learning - Supervised", "topics": ["Linear Regression", "Logistic Regression", "Decision Trees", "Random Forest", "SVM"]},
        {"module_number": 4, "module_title": "Machine Learning - Unsupervised", "topics": ["K-Means Clustering", "PCA", "Hierarchical Clustering", "Association Rules"]},
        {"module_number": 5, "module_number": 5, "module_title": "Deep Learning Fundamentals", "topics": ["Artificial Neural Networks", "Backpropagation", "Optimizers", "Activation Functions"]},
        {"module_number": 6, "module_title": "Computer Vision (CV)", "topics": ["CNN Architecture", "Object Detection", "YOLO", "Image Segmentation", "OpenCV"]},
        {"module_number": 7, "module_title": "Natural Language Processing (NLP)", "topics": ["Tokenization", "BERT", "Transformers", "Sentiment Analysis", "NLTK"]},
        {"module_number": 8, "module_title": "Generative AI & LLMs", "topics": ["Prompt Engineering", "RAG Pipeline", "Fine-tuning Models", "LangChain", "Vector Databases"]},
        {"module_number": 9, "module_title": "Data Engineering & Cloud", "topics": ["AWS S3", "Docker", "Kubernetes", "Flask API", "MLOps Pipelines"]},
        {"module_number": 10, "module_title": "Capstone Projects & Portfolio", "topics": ["Real-time Fraud Detection", "Healthcare AI", "Sales Prediction", "GitHub Portfolio"]}
      ],
      "learning_outcomes": [
        "Master end-to-end ML & AI development",
        "Deploy production-grade AI models on Cloud",
        "Create a professional GitHub portfolio with 5+ live projects",
        "Expertise in Generative AI and LLM integration"
      ],
      "tools_technologies": ["Python", "PyTorch", "TensorFlow", "Azure AI", "AWS", "Docker", "Kubernetes", "LangChain", "OpenAI API"],
      "industry_scope": ["BFSI", "Healthcare", "E-commerce", "FinTech", "Supply Chain", "Automotive"],
      "job_roles": ["Data Scientist", "ML Engineer", "AI Researcher", "Data Engineer", "LLM Developer"],
      "partners": ["Google Cloud", "NVIDIA", "AWS", "Microsoft", "Meta"],
      "accreditation": "ISO 9001:2015 Certified",
      "naac_grade": "A+",
      "placement_support": "100% Placement Assistance with 500+ Global Hiring Partners",
      "faqs": [
        {
          "question": "Is there a weekend batch?",
          "answer": "Yes, we have specialized weekend batches for working professionals."
        },
        {
          "question": "Do I need a coding background?",
          "answer": "While helpful, we start from scratch with Python to ensure everyone can follow along."
        }
      ],
      "other_highlights": ["Live Projects", "LMS Access", "Resume Building Workshop", "Mock Interviews", "Lifetime Access to Alumni Network"]
    }

    import json
    new_doc = KnowledgeBaseDocument(
        institute_id=institute_id,
        file_name=file.filename,
        file_url=f"/static/knowledge/{institute_id}_{file.filename}",
        status="processed",
        ai_report=json.dumps(mock_extracted_data)
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
