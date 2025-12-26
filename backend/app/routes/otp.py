"""OTP routes for verification."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import OTPSendRequest, OTPVerifyRequest, OTPResponse
from app.services.otp_service import otp_service
from app.models.database import AuditLog
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/otp", tags=["OTP"])


@router.post("/send", response_model=OTPResponse)
def send_otp(request: OTPSendRequest, db: Session = Depends(get_db)):
    """
    Send OTP to user via SMS, WhatsApp, or email.
    
    - **phone_or_email**: Phone number or email address
    - **channel**: Communication channel ('sms', 'whatsapp', 'email')
    - **reporter_id**: Optional reporter ID
    """
    try:
        result = otp_service.send_otp(
            db=db,
            phone_or_email=request.phone_or_email,
            channel=request.channel,
            reporter_id=request.reporter_id
        )
        
        # Log audit trail
        audit = AuditLog(
            reporter_id=request.reporter_id,
            action="OTP_SENT",
            channel=request.channel,
            meta={"phone_or_email": request.phone_or_email}
        )
        db.add(audit)
        db.commit()
        
        return OTPResponse(**result)
        
    except Exception as e:
        logger.error(f"Error sending OTP: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send OTP")


@router.post("/verify", response_model=OTPResponse)
def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    """
    Verify OTP entered by user.
    
    - **phone_or_email**: Phone number or email address
    - **otp**: OTP code entered by user
    """
    try:
        result = otp_service.verify_otp(
            db=db,
            phone_or_email=request.phone_or_email,
            otp=request.otp
        )
        
        # Log audit trail
        audit = AuditLog(
            action="OTP_VERIFY_ATTEMPT",
            meta={
                "phone_or_email": request.phone_or_email,
                "success": result["success"]
            }
        )
        db.add(audit)
        db.commit()
        
        return OTPResponse(**result)
        
    except Exception as e:
        logger.error(f"Error verifying OTP: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to verify OTP")
