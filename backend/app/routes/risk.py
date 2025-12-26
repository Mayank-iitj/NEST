"""Risk scoring routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import RiskScoreResponse
from app.services.risk_service import risk_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/risk", tags=["Risk"])


@router.get("/score/{event_id}", response_model=RiskScoreResponse)
def get_risk_score(event_id: int, db: Session = Depends(get_db)):
    """
    Calculate and retrieve risk score for an event.
    
    Returns risk score (0-100), classification, and hospitalization/mortality probabilities.
    """
    try:
        result = risk_service.calculate_and_update_risk(db, event_id)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting risk score: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to calculate risk score")
