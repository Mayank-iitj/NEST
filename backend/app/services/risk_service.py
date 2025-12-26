"""Risk scoring service for adverse events."""
from sqlalchemy.orm import Session
from app.models.database import Event
from app.services.ai_service import ai_service
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class RiskService:
    """Risk assessment and scoring service."""
    
    @staticmethod
    def calculate_and_update_risk(db: Session, event_id: int) -> Dict[str, Any]:
        """
        Calculate risk score for an event and update the database.
        
        Args:
            db: Database session
            event_id: Event ID
            
        Returns:
            Dictionary with risk assessment results
        """
        event = db.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            return {"error": "Event not found"}
        
        # Prepare event data for AI analysis
        event_data = {
            "suspected_drug": event.suspected_drug,
            "adverse_effect": event.adverse_effect,
            "seriousness": event.seriousness,
            "hospitalization": event.hospitalization,
            "outcome": event.outcome,
            "comorbidities": event.comorbidities
        }
        
        # Get AI risk assessment
        risk_result = ai_service.calculate_risk_score(event_data)
        
        # Update event with risk scores
        event.risk_score = risk_result.get("score", 50)
        event.risk_class = risk_result.get("class", "medium")
        event.hospitalization_risk = risk_result.get("hospitalization_risk", 0.3)
        event.mortality_risk = risk_result.get("mortality_risk", 0.1)
        
        # Update followup status based on risk
        if event.risk_class in ["high", "critical"]:
            event.followup_status = "escalated"
        
        db.commit()
        db.refresh(event)
        
        logger.info(f"Risk calculated for event {event_id}: {event.risk_class} ({event.risk_score})")
        
        return {
            "event_id": event.id,
            "risk_score": event.risk_score,
            "risk_class": event.risk_class,
            "hospitalization_risk": event.hospitalization_risk,
            "mortality_risk": event.mortality_risk,
            "reasoning": risk_result.get("reasoning", "")
        }
    
    @staticmethod
    def detect_and_store_missing_fields(db: Session, event_id: int) -> Dict[str, Any]:
        """
        Detect missing fields for an event using AI.
        
        Args:
            db: Database session
            event_id: Event ID
            
        Returns:
            Dictionary with missing fields analysis
        """
        event = db.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            return {"error": "Event not found"}
        
        # Prepare event data
        event_data = {
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
        
        # Get AI analysis
        missing_fields_result = ai_service.detect_missing_fields(event_data)
        
        # Store missing fields in event
        all_missing = missing_fields_result.get("required_fields", []) + missing_fields_result.get("optional_fields", [])
        event.missing_fields = all_missing
        
        db.commit()
        
        logger.info(f"Missing fields detected for event {event_id}: {len(all_missing)} fields")
        
        return missing_fields_result


# Export singleton instance
risk_service = RiskService()
