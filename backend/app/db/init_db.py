import uuid
from sqlalchemy.orm import Session
from app.core import security
from app.models.institute import Institute
from app.models.user import User, UserRole
from app.models.bookings_settings import Settings

def init_db(db: Session) -> None:
    # 1. Create Default Institute
    institute = db.query(Institute).filter(Institute.name == "Admin University").first()
    if not institute:
        institute = Institute(
            name="Admin University",
            email="admin@university.com",
            onboarding_status=True,
            onboarding_step=4
        )
        db.add(institute)
        db.commit()
        db.refresh(institute)
        
        # Create default settings for the institute
        settings = Settings(
            institute_id=institute.id,
            timezone="UTC",
            notifications={"dailySummary": True, "leadAlerts": True, "handoffAlerts": True, "healthAlerts": True}
        )
        db.add(settings)
        db.commit()

    # 2. Create Default Super Admin
    user = db.query(User).filter(User.email == "admin@university.com").first()
    if not user:
        user = User(
            email="admin@university.com",
            password_hash=security.get_password_hash("admin123"),
            name="Super Admin",
            role=UserRole.super_admin,
            institute_id=institute.id,
            is_active=True
        )
        db.add(user)
        db.commit()
        print(f"Created initial super_admin: {user.email}")
