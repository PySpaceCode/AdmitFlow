from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.bookings_settings import Booking
from app.models.leads import Lead
from app.schemas.settings_bookings import BookingUpdateRequest

router = APIRouter()

@router.get("/")
def get_bookings(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    return db.query(Booking).join(Lead).filter(Lead.institute_id == institute_id).all()

@router.post("/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    update_data: BookingUpdateRequest,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    b = db.query(Booking).join(Lead).filter(
        Booking.id == booking_id, 
        Lead.institute_id == institute_id
    ).first()
    
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    b.status = update_data.status
    b.agent_assigned_id = update_data.agentAssignedId
        
    db.add(b)
    db.commit()
    db.refresh(b)
    
    return {
        "success": True,
        "message": "Booking updated",
        "data": {
            "bookingId": b.id,
            "status": b.status,
            "agentAssignedId": b.agent_assigned_id
        }
    }
