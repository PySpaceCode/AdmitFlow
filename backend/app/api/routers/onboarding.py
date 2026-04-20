from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.onboarding import OnboardingSetupRequest
from app.models.institute import Institute
from app.models.user import User

router = APIRouter()

@router.get("/status")
def get_status(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    institute = db.query(Institute).filter(Institute.id == institute_id).first()
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
        
    return {
        "onboardingStatus": institute.onboarding_status,
        "progress": 100 if institute.onboarding_status else 50
    }

@router.post("/setup")
def setup_institute(
    setup_data: OnboardingSetupRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    institute = db.query(Institute).filter(Institute.id == current_user.institute_id).first()
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
        
    institute.name = setup_data.instituteName
    institute.onboarding_status = True
    
    # Also update user info as per setup request
    current_user.full_name = setup_data.fullName
    current_user.email = setup_data.email
    
    db.add(institute)
    db.add(current_user)
    db.commit()
    db.refresh(institute)
    
    return {
        "success": True,
        "message": "Onboarding completed",
        "data": {
            "instituteId": institute.id,
            "onboardingStatus": institute.onboarding_status
        }
    }
