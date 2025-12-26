"""Report routes for adverse event submission."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import (
    ReporterCreate, ReporterResponse,
    EventCreate, EventResponse,
    MissingFieldsResponse,
    RegulatoryNarrative
)
from app.models.database import Reporter, Event, AuditLog
from app.services.risk_service import risk_service
from app.services.ai_service import ai_service
from typing import List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/report", tags=["Reports"])


@router.post("/reporter", response_model=ReporterResponse)
def create_reporter(reporter: ReporterCreate, db: Session = Depends(get_db)):
    """
    Create a new reporter (patient or HCP).
    
    - **reporter_type**: 'patient' or 'hcp'
    - **name**: Reporter's name
    - **phone**: Phone number
    - **email**: Email address
    - **language**: Preferred language code
    """
    try:
        db_reporter = Reporter(**reporter.model_dump())
        db.add(db_reporter)
        db.commit()
        db.refresh(db_reporter)
        
        # Log audit trail
        audit = AuditLog(
            reporter_id=db_reporter.id,
            action="REPORTER_CREATED",
            meta={"reporter_type": reporter.reporter_type}
        )
        db.add(audit)
        db.commit()
        
        logger.info(f"Reporter created: {db_reporter.id}")
        return db_reporter
        
    except Exception as e:
        logger.error(f"Error creating reporter: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create reporter")


@router.post("/init", response_model=EventResponse)
def initialize_report(event: EventCreate, db: Session = Depends(get_db)):
    """
    Initialize a new adverse event report.
    
    Accepts initial event data, detects missing fields, and calculates risk score.
    """
    try:
        # Create event
        db_event = Event(**event.model_dump())
        db_event.followup_status = "pending"
        
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        
        # Detect missing fields using AI
        missing_fields = risk_service.detect_and_store_missing_fields(db, db_event.id)
        
        # Calculate risk score
        risk_assessment = risk_service.calculate_and_update_risk(db, db_event.id)
        
        # Log audit trail
        audit = AuditLog(
            event_id=db_event.id,
            reporter_id=db_event.reporter_id,
            action="EVENT_CREATED",
            meta={
                "risk_class": db_event.risk_class,
                "missing_fields_count": len(db_event.missing_fields or [])
            }
        )
        db.add(audit)
        db.commit()
        
        # Refresh to get updated data
        db.refresh(db_event)
        
        logger.info(f"Event initialized: {db_event.id}, risk: {db_event.risk_class}")
        return db_event
        
    except Exception as e:
        logger.error(f"Error initializing report: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to initialize report")


@router.get("/event/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get event details by ID."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/missing-fields/{event_id}", response_model=MissingFieldsResponse)
def detect_missing_fields(event_id: int, db: Session = Depends(get_db)):
    """
    Detect missing regulatory-relevant fields for an event.
    
    Uses AI to analyze the event and identify required and optional missing fields.
    """
    try:
        result = risk_service.detect_and_store_missing_fields(db, event_id)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        # Log audit trail
        audit = AuditLog(
            event_id=event_id,
            action="MISSING_FIELDS_DETECTED",
            meta=result
        )
        db.add(audit)
        db.commit()
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error detecting missing fields: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to detect missing fields")


@router.get("/narrative/{event_id}", response_model=RegulatoryNarrative)
def generate_narrative(event_id: int, db: Session = Depends(get_db)):
    """
    Generate ICSR-ready regulatory narrative for an event.
    
    Uses AI to create a formal pharmacovigilance summary.
    """
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Prepare event data
        event_data = {
            "reporter_type": event.reporter.reporter_type if event.reporter else "unknown",
            "suspected_drug": event.suspected_drug,
            "dose": event.dose,
            "frequency": event.frequency,
            "start_date": str(event.start_date) if event.start_date else None,
            "stop_date": str(event.stop_date) if event.stop_date else None,
            "adverse_effect": event.adverse_effect,
            "seriousness": event.seriousness,
            "hospitalization": event.hospitalization,
            "outcome": event.outcome,
            "comorbidities": event.comorbidities,
            "medications": event.medications
        }
        
        # Generate narrative
        narrative = ai_service.generate_regulatory_summary(event_data)
        
        # Log audit trail
        audit = AuditLog(
            event_id=event_id,
            action="NARRATIVE_GENERATED",
            meta={"narrative_length": len(narrative)}
        )
        db.add(audit)
        db.commit()
        
        return {
            "event_id": event_id,
            "narrative": narrative,
            "generated_at": datetime.utcnow()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating narrative: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate narrative")
