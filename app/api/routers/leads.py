from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from app.api import deps
from app.models.leads import Lead
from app.models.campaign import Campaign
from app.schemas.leads import CampaignLaunchRequest

router = APIRouter()

@router.get("/")
def get_leads(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    return db.query(Lead).filter(Lead.institute_id == institute_id).all()

@router.post("/upload-csv")
async def upload_leads_csv(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    content = await file.read()
    try:
        decoded = content.decode('utf-8-sig')
    except UnicodeDecodeError:
        decoded = content.decode('latin-1')
        
    reader = csv.DictReader(io.StringIO(decoded))
    
    total_records = 0
    saved_leads = 0
    
    for row in reader:
        total_records += 1
        # Normalize keys to lowercase for flexible CSV headers
        row = {k.lower().strip(): v for k, v in row.items()}
        
        phone = row.get('phone', '').strip()
        if not phone: continue
        
        # Check for duplicates within the same institute
        existing = db.query(Lead).filter(Lead.phone == phone, Lead.institute_id == institute_id).first()
        if existing:
            continue
        
        new_lead = Lead(
            institute_id=institute_id,
            name=row.get('name', 'Unknown'),
            phone=phone,
            email=row.get('email'),
            course=row.get('course'),
            status="new"
        )
        db.add(new_lead)
        saved_leads += 1
    
    db.commit()
    
    return {
        "success": True,
        "message": "Leads uploaded",
        "data": {
            "totalRecords": total_records,
            "savedLeads": saved_leads
        }
    }

@router.post("/campaign/launch")
def launch_campaign(
    launch_data: CampaignLaunchRequest,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    new_campaign = Campaign(
        institute_id=institute_id,
        calling_days=launch_data.callingDays,
        time_start=launch_data.timeStart,
        time_end=launch_data.timeEnd,
        max_attempts=launch_data.maxAttempts,
        fallback_name=launch_data.fallbackName,
        fallback_phone=launch_data.fallbackPhone,
        status="active"
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    
    return {
        "success": True,
        "message": "Campaign launched",
        "data": {
            "campaignId": new_campaign.id,
            "status": new_campaign.status
        }
    }
