from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.api import deps
from app.models.leads import Lead
from app.models.calls import Call
from app.models.bookings_settings import Booking

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    institute_id: int = Depends(deps.get_current_institute_id)
):
    # Overall stats
    total_leads = db.query(Lead).filter(Lead.institute_id == institute_id).count()
    calls_made = db.query(Call).filter(Call.institute_id == institute_id).count()
    bookings_confirmed = db.query(Booking).join(Lead).filter(
        Lead.institute_id == institute_id,
        Booking.status.in_(["confirmed", "Confirmed"])
    ).count()
    
    conversion_rate = 0
    if total_leads > 0:
        conversion_rate = round((bookings_confirmed / total_leads) * 100, 1)
    
    # Recent activity
    # Fetch 5 most recent calls
    recent_calls = db.query(Call).filter(Call.institute_id == institute_id).order_by(Call.created_at.desc()).limit(5).all()
    # Fetch 5 most recent bookings
    recent_bookings = db.query(Booking).join(Lead).filter(Lead.institute_id == institute_id).order_by(Booking.created_at.desc()).limit(5).all()
    
    activity = []
    for c in recent_calls:
        activity.append({
            "type": "call",
            "action": f"Call with {c.lead.name if c.lead else 'Unknown'}",
            "time": c.created_at.isoformat(),
            "sentiment": c.sentiment
        })
        
    for b in recent_bookings:
        activity.append({
            "type": "booking",
            "action": f"Booking confirmed for {b.lead.name if b.lead else 'Unknown'}",
            "time": b.created_at.isoformat(),
            "status": b.status
        })
        
    # Sort by time desc
    activity.sort(key=lambda x: x["time"], reverse=True)
    activity = activity[:5]
    
    # Simple Chart Data (Last 7 Days)
    chart_data = []
    today = datetime.now().date()
    for i in range(6, -1, -1):
        target_date = today - timedelta(days=i)
        date_str = target_date.strftime("%a")
        
        # Count calls on this day
        connected = db.query(Call).filter(
            Call.institute_id == institute_id,
            func.date(Call.created_at) == target_date,
            Call.status == "completed"
        ).count()
        
        failed = db.query(Call).filter(
            Call.institute_id == institute_id,
            func.date(Call.created_at) == target_date,
            Call.status != "completed"
        ).count()
        
        chart_data.append({
            "day": date_str,
            "connected": connected,
            "failed": failed,
            "max": 50 # Default max for visual scaling
        })
        
    # Get upcoming bookings for the panel
    upcoming_bookings = db.query(Booking).join(Lead).filter(
        Lead.institute_id == institute_id,
        Booking.status.in_(["confirmed", "Confirmed", "pending", "Pending"])
    ).order_by(func.coalesce(Booking.scheduled_at, Booking.created_at).asc()).limit(5).all()
    
    formatted_bookings = []
    for b in upcoming_bookings:
        display_time = b.scheduled_at or b.created_at
        formatted_bookings.append({
            "lead_name": b.lead.name if b.lead else "Unknown",
            "course": b.lead.course if b.lead else "N/A",
            "datetime": display_time.strftime("%Y-%m-%d %H:%M"),
            "status": b.status.capitalize()
        })

    return {
        "success": True,
        "data": {
            "stats": {
                "total_leads": total_leads,
                "calls_made": calls_made,
                "bookings": bookings_confirmed,
                "conversion_rate": f"{conversion_rate}%"
            },
            "activity": activity,
            "bookings": formatted_bookings,
            "chartData": chart_data
        }
    }
