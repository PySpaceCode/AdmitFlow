from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    calling_days = Column(JSON, nullable=False) # e.g., ["Mon", "Tue", "Wed"]
    time_start = Column(String, nullable=False) # e.g., "10:00"
    time_end = Column(String, nullable=False)   # e.g., "17:00"
    max_attempts = Column(Integer, default=2)
    fallback_name = Column(String, nullable=True) # Added as per schema
    fallback_phone = Column(String, nullable=True) # Added as per schema
    status = Column(String, default="active")   # active, paused, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    institute = relationship("Institute", backref="campaigns")
