"""SQLAlchemy ORM models for the database."""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, Date, DateTime, ForeignKey, JSON, LargeBinary
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Reporter(Base):
    """Reporter model (patients and healthcare professionals)."""
    __tablename__ = "reporters"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    reporter_type = Column(String(20), nullable=False)  # 'patient' or 'hcp'
    name = Column(Text)
    phone = Column(Text, index=True)
    email = Column(Text, index=True)
    language = Column(String(10), default='en')
    verified = Column(Boolean, default=False, index=True)
    encrypted_data = Column(LargeBinary)  # AES-256 encrypted PHI
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    events = relationship("Event", back_populates="reporter", cascade="all, delete-orphan")
    otp_tokens = relationship("OTPToken", back_populates="reporter", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="reporter")


class Event(Base):
    """Adverse event model."""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    reporter_id = Column(Integer, ForeignKey("reporters.id", ondelete="CASCADE"), index=True)
    
    # Drug information
    suspected_drug = Column(Text)
    dose = Column(Text)
    frequency = Column(Text)
    start_date = Column(Date)
    stop_date = Column(Date)
    
    # Adverse effect details
    adverse_effect = Column(Text)
    seriousness = Column(String(20))  # 'serious', 'non-serious', 'unknown'
    hospitalization = Column(Boolean)
    outcome = Column(Text)  # 'recovered', 'recovering', 'not_recovered', 'fatal', 'unknown'
    
    # Medical context
    comorbidities = Column(Text)
    medications = Column(Text)  # Concomitant medications
    
    # Follow-up management
    followup_status = Column(String(20), default='pending', index=True)
    missing_fields = Column(JSONB)  # Array of missing field names
    
    # Consent and compliance
    consent = Column(Boolean, default=False)
    consent_timestamp = Column(DateTime(timezone=True))
    
    # Risk scoring
    risk_score = Column(Float)
    risk_class = Column(String(20), index=True)  # 'low', 'medium', 'high', 'critical'
    hospitalization_risk = Column(Float)
    mortality_risk = Column(Float)
    
    # Metadata
    encrypted_data = Column(LargeBinary)  # AES-256 encrypted PHI
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    reporter = relationship("Reporter", back_populates="events")
    audit_logs = relationship("AuditLog", back_populates="event", cascade="all, delete-orphan")
    followup_questions = relationship("FollowupQuestion", back_populates="event", cascade="all, delete-orphan")


class OTPToken(Base):
    """OTP token model for verification."""
    __tablename__ = "otp_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("reporters.id", ondelete="CASCADE"), index=True)
    token_hash = Column(String(255), nullable=False)  # Hashed OTP
    channel = Column(String(20), nullable=False)  # 'sms', 'whatsapp', 'email'
    phone_or_email = Column(Text, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime(timezone=True))
    attempts = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reporter = relationship("Reporter", back_populates="otp_tokens")


class AuditLog(Base):
    """Audit log model for compliance tracking."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), index=True, nullable=True)
    reporter_id = Column(Integer, ForeignKey("reporters.id"), nullable=True)
    action = Column(Text, nullable=False)
    channel = Column(Text)
    user_role = Column(String(50))
    ip_address = Column(String(45))
    meta = Column(JSONB)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    event = relationship("Event", back_populates="audit_logs")
    reporter = relationship("Reporter", back_populates="audit_logs")


class FollowupQuestion(Base):
    """Follow-up questions sent to users."""
    __tablename__ = "followup_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), index=True)
    question_text = Column(Text, nullable=False)
    question_language = Column(String(10), default='en')
    field_name = Column(Text)  # Which missing field this question addresses
    channel = Column(String(20))  # 'sms', 'whatsapp', 'email'
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    answered = Column(Boolean, default=False)
    answer_text = Column(Text)
    answered_at = Column(DateTime(timezone=True))
    
    # Relationships
    event = relationship("Event", back_populates="followup_questions")
