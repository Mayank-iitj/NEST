"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


class ReporterType(str, Enum):
    """Reporter type enumeration."""
    PATIENT = "patient"
    HCP = "hcp"


class Seriousness(str, Enum):
    """Seriousness level enumeration."""
    SERIOUS = "serious"
    NON_SERIOUS = "non-serious"
    UNKNOWN = "unknown"


class Outcome(str, Enum):
    """Outcome enumeration."""
    RECOVERED = "recovered"
    RECOVERING = "recovering"
    NOT_RECOVERED = "not_recovered"
    FATAL = "fatal"
    UNKNOWN = "unknown"


class RiskClass(str, Enum):
    """Risk classification enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Channel(str, Enum):
    """Communication channel enumeration."""
    SMS = "sms"
    WHATSAPP = "whatsapp"
    EMAIL = "email"


# Reporter schemas
class ReporterBase(BaseModel):
    """Base reporter schema."""
    reporter_type: ReporterType
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    language: str = "en"


class ReporterCreate(ReporterBase):
    """Schema for creating a reporter."""
    pass


class ReporterResponse(ReporterBase):
    """Schema for reporter response."""
    id: int
    uuid: str
    verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Event schemas
class EventBase(BaseModel):
    """Base event schema."""
    suspected_drug: Optional[str] = None
    dose: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    stop_date: Optional[date] = None
    adverse_effect: Optional[str] = None
    seriousness: Optional[Seriousness] = None
    hospitalization: Optional[bool] = None
    outcome: Optional[Outcome] = None
    comorbidities: Optional[str] = None
    medications: Optional[str] = None


class EventCreate(EventBase):
    """Schema for creating an event."""
    reporter_id: int
    consent: bool = False


class EventResponse(EventBase):
    """Schema for event response."""
    id: int
    uuid: str
    reporter_id: int
    followup_status: str
    missing_fields: Optional[List[str]] = None
    risk_score: Optional[float] = None
    risk_class: Optional[RiskClass] = None
    hospitalization_risk: Optional[float] = None
    mortality_risk: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# OTP schemas
class OTPSendRequest(BaseModel):
    """Schema for sending OTP."""
    phone_or_email: str
    channel: Channel
    reporter_id: Optional[int] = None


class OTPVerifyRequest(BaseModel):
    """Schema for verifying OTP."""
    phone_or_email: str
    otp: str


class OTPResponse(BaseModel):
    """Schema for OTP response."""
    success: bool
    message: str
    token: Optional[str] = None


# Follow-up schemas
class FollowupQuestionCreate(BaseModel):
    """Schema for creating a follow-up question."""
    event_id: int
    question_text: str
    field_name: str
    channel: Channel
    language: str = "en"


class FollowupAnswerRequest(BaseModel):
    """Schema for answering a follow-up question."""
    question_id: int
    answer_text: str
    token: str


class FollowupQuestionResponse(BaseModel):
    """Schema for follow-up question response."""
    id: int
    event_id: int
    question_text: str
    field_name: str
    answered: bool
    answer_text: Optional[str] = None
    sent_at: datetime
    
    class Config:
        from_attributes = True


# Risk scoring schemas
class RiskScoreResponse(BaseModel):
    """Schema for risk score response."""
    event_id: int
    risk_score: float
    risk_class: RiskClass
    hospitalization_risk: float
    mortality_risk: float
    reasoning: str


# Missing fields detection
class MissingFieldsResponse(BaseModel):
    """Schema for missing fields response."""
    required_fields: List[str]
    optional_fields: List[str]
    risk_reasoning: str


# Dashboard metrics
class DashboardMetrics(BaseModel):
    """Schema for dashboard metrics."""
    total_events: int
    response_rate_increase: float
    missing_field_reduction: float
    cycle_time_reduction: float
    high_risk_accuracy: float
    agent_workload_reduction: float
    high_risk_count: int
    pending_followups: int


# Export schemas
class ExportRequest(BaseModel):
    """Schema for export request."""
    format: str = Field(..., pattern="^(csv|pdf|json)$")
    event_ids: Optional[List[int]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None


# AI-generated summary
class RegulatoryNarrative(BaseModel):
    """Schema for regulatory narrative."""
    event_id: int
    narrative: str
    generated_at: datetime
