from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
from sqlalchemy.dialects.postgresql import JSONB

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="SET NULL"), nullable=True, index=True)
    status = Column(String, default="completed") # completed, failed, no_answer, busy
    sentiment = Column(String, nullable=True)    # positive, neutral, negative
    duration = Column(Integer, nullable=True)     # in seconds
    summary = Column(Text, nullable=True)
    transcript = Column(JSONB, nullable=True)
    handoff_log = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    institute = relationship("Institute", backref="calls")
    lead = relationship("Lead", backref="calls")
