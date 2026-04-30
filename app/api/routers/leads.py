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

@router.get("/")
def get_leads(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    return db.query(Lead).filter(Lead.institute_id == institute_id).all()

@router.post("/upload_leads")
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
        if existing:
            skipped_leads += 1
            continue
        
        new_lead = Lead(
            institute_id=institute_id,
            name=str(row.get('name', 'Unknown')).strip(),
            phone=phone,
            email=str(row.get('email', '')).strip() if pd.notna(row.get('email')) else None,
            course=str(row.get('course', '')).strip() if pd.notna(row.get('course')) else None,
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

@router.post("/calling_configuration")
def configure_calling(
    config_data: CallingConfigurationRequest,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
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
    db.commit()
    db.refresh(new_campaign)
    
    return {
        "success": True,
        "message": "Calling configuration saved",
        "data": {
            "campaignId": new_campaign.id,
            "status": new_campaign.status
        }
    }
