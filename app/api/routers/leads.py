from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import io
import logging
import pandas as pd
from app.api import deps
from app.models.leads import Lead
from app.models.campaign import Campaign
from app.schemas.leads import CallingConfigurationRequest

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", summary="Get all leads for your institute")
def get_leads(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    return db.query(Lead).filter(Lead.institute_id == institute_id).all()

@router.post("/upload", summary="Upload leads from CSV or Excel file")
async def upload_leads_file(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    logger.info(f"Uploading leads for institute {institute_id}, file: {file.filename}")
    content = await file.read()
    
    try:
        if file.filename.endswith('.csv'):
            try:
                decoded = content.decode('utf-8-sig')
            except UnicodeDecodeError:
                decoded = content.decode('latin-1')
            df = pd.read_csv(io.StringIO(decoded))
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        # Standardize columns
        df.columns = [str(c).lower().strip() for c in df.columns]
        logger.info(f"Found columns: {list(df.columns)}")
        
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    total_records = 0
    saved_leads = 0
    skipped_leads = 0
    
    for index, row in df.iterrows():
        total_records += 1
        
        # Handle phone number conversion (especially for Excel numeric values)
        phone_val = row.get('phone')
        if pd.isna(phone_val):
            skipped_leads += 1
            continue
            
        # If it's a float (like 9199999999.0), convert to int then str to avoid .0
        if isinstance(phone_val, float):
            phone = str(int(phone_val))
        else:
            phone = str(phone_val).strip()
            
        if not phone or phone == 'nan':
            skipped_leads += 1
            continue
        
        # Check for duplicates within the same institute
        existing = db.query(Lead).filter(Lead.phone == phone, Lead.institute_id == institute_id).first()
        
        # Support common column variations
        name_val = str(row.get('name') or row.get('student name') or row.get('full name') or 'Unknown').strip()
        course_val = row.get('course') or row.get('course interest') or row.get('subject') or ''

        if existing:
            # If the existing lead has an "Unknown" name, update it with the new name
            if existing.name == "Unknown" and name_val != "Unknown":
                existing.name = name_val
                if not existing.course and course_val:
                    existing.course = str(course_val).strip()
                db.add(existing)
                saved_leads += 1
            else:
                skipped_leads += 1
            continue
        
        new_lead = Lead(
            institute_id=institute_id,
            name=str(name_val).strip(),
            phone=phone,
            email=str(row.get('email', '')).strip() if pd.notna(row.get('email')) else None,
            course=str(course_val).strip() if course_val else None,
            status="Pending"
        )
        db.add(new_lead)
        saved_leads += 1
    
    try:
        db.commit()
        logger.info(f"Successfully saved {saved_leads} leads. Total: {total_records}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error committing leads: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error while saving leads")
    
    return {
        "success": True,
        "message": f"Successfully uploaded {saved_leads} leads",
        "data": {
            "totalRecords": total_records,
            "savedLeads": saved_leads,
            "skippedLeads": skipped_leads
        }
    }

@router.post("/calling-config", summary="Set calling schedule and agent configuration")
def configure_calling(
    config_data: CallingConfigurationRequest,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    # Check if a campaign already exists for this institute
    existing_campaign = db.query(Campaign).filter(Campaign.institute_id == institute_id).first()
    
    if existing_campaign:
        # Update existing campaign
        existing_campaign.calling_days = config_data.calling_days
        existing_campaign.time_start = config_data.calling_window_start
        existing_campaign.time_end = config_data.calling_window_end
        existing_campaign.max_attempts = config_data.maximum_daily_call_attempts
        existing_campaign.fallback_name = config_data.human_agent_name
        existing_campaign.fallback_phone = config_data.human_agent_phone_number
        existing_campaign.status = "active"
        db.add(existing_campaign)
        campaign = existing_campaign
    else:
        # Create new campaign
        new_campaign = Campaign(
            institute_id=institute_id,
            calling_days=config_data.calling_days,
            time_start=config_data.calling_window_start,
            time_end=config_data.calling_window_end,
            max_attempts=config_data.maximum_daily_call_attempts,
            fallback_name=config_data.human_agent_name,
            fallback_phone=config_data.human_agent_phone_number,
            status="active"
        )
        db.add(new_campaign)
        campaign = new_campaign
        
    db.commit()
    db.refresh(campaign)
    
    return {
        "success": True,
        "message": "Calling configuration saved",
        "data": {
            "campaignId": campaign.id,
            "status": campaign.status
        }
    }
