from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.bookings_settings import Settings
from app.schemas.settings_bookings import SettingsSaveRequest

router = APIRouter()

@router.get("/")
def get_settings(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    s = db.query(Settings).filter(Settings.institute_id == institute_id).first()
    if not s or not s.config:
        return {"whatsappEnabled": True, "callEnabled": True}
    return s.config

@router.post("/save")
def save_settings(
    settings_data: SettingsSaveRequest,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    s = db.query(Settings).filter(Settings.institute_id == institute_id).first()
    if not s:
        s = Settings(institute_id=institute_id)
    
    s.config = {
        "whatsappEnabled": settings_data.whatsappEnabled,
        "callEnabled": settings_data.callEnabled
    }
    
    db.add(s)
    db.commit()
    db.refresh(s)
    
    return {
        "success": True,
        "message": "Settings saved",
        "data": s.config
    }
