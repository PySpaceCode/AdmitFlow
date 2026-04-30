from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.session import Base

class Institute(Base):
    __tablename__ = "institutes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True) # Added as per schema
    phone = Column(String, nullable=True) # Added for onboarding setup
    institute_type = Column(String, nullable=True)
    city_address = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    email_verification = Column(String, nullable=True)
    phone_verification = Column(String, nullable=True)
    social_fb = Column(String, nullable=True)
    social_ig = Column(String, nullable=True)
    social_linkedin = Column(String, nullable=True)
    social_x = Column(String, nullable=True)
    onboarding_status = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
