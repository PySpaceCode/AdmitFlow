from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.bookings_settings import Booking
from app.models.leads import Lead
from app.schemas.settings_bookings import BookingUpdateRequest, BookingWithLead, BookingRescheduleRequest
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[BookingWithLead])
def get_bookings(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    bookings = db.query(Booking).join(Lead).outerjoin(User, Booking.agent_assigned_id == User.id).filter(
        Lead.institute_id == institute_id
    ).all()
    
    results = []
    for b in bookings:
        results.append(BookingWithLead(
            id=b.id,
            status=b.status,
            scheduled_at=b.scheduled_at,
            created_at=b.created_at,
            lead_name=b.lead.name,
            lead_phone=b.lead.phone,
            lead_course=b.lead.course,
            agent_name=b.agent.username if b.agent else "Unassigned"
        ))
    return results

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

@router.post("/{booking_id}/reschedule")
def reschedule_booking(
    booking_id: int,
    reschedule_data: BookingRescheduleRequest,
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    b = db.query(Booking).join(Lead).filter(
        Booking.id == booking_id, 
        Lead.institute_id == institute_id
    ).first()
    
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    b.scheduled_at = reschedule_data.scheduledAt
    
    db.add(b)
    db.commit()
    db.refresh(b)
    
    return {
        "success": True,
        "message": "Booking rescheduled successfully",
        "data": {
            "bookingId": b.id,
            "scheduledAt": b.scheduled_at
        }
    }
