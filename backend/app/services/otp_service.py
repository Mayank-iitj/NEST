"""OTP service for generating and verifying one-time passwords."""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.database import OTPToken, Reporter
from app.core.security import generate_otp, hash_otp, verify_otp
from app.core.config import settings
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class OTPService:
    """OTP management service."""
    
    @staticmethod
    def send_otp(
        db: Session,
        phone_or_email: str,
        channel: str,
        reporter_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate and send OTP to user.
        
        Args:
            db: Database session
            phone_or_email: Phone number or email address
            channel: 'sms', 'whatsapp', or 'email'
            reporter_id: Optional reporter ID
            
        Returns:
            Dictionary with success status and message
        """
        from app.services.messaging_service import messaging_service
        
        # Generate OTP
        otp = generate_otp(settings.OTP_LENGTH)
        otp_hash = hash_otp(otp)
        
        # Set expiry
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        
        # Store in database
        otp_token = OTPToken(
            reporter_id=reporter_id,
            token_hash=otp_hash,
            channel=channel,
            phone_or_email=phone_or_email,
            expires_at=expires_at
        )
        db.add(otp_token)
        db.commit()
        
        # Send OTP via appropriate channel
        message = f"""🏥 Your verification code is: {otp}

This code expires in {settings.OTP_EXPIRE_MINUTES} minutes.

🛡️ Never share this code with anyone.
✅ We will never ask for payment."""
        
        success = messaging_service.send_message(
            to=phone_or_email,
            message=message,
            channel=channel
        )
        
        if success:
            logger.info(f"OTP sent via {channel} to {phone_or_email}")
            return {"success": True, "message": "OTP sent successfully", "expires_in": settings.OTP_EXPIRE_MINUTES}
        else:
            logger.error(f"Failed to send OTP via {channel} to {phone_or_email}")
            return {"success": False, "message": "Failed to send OTP"}
    
    @staticmethod
    def verify_otp(db: Session, phone_or_email: str, otp: str) -> Dict[str, Any]:
        """
        Verify OTP entered by user.
        
        Args:
            db: Database session
            phone_or_email: Phone number or email address
            otp: OTP entered by user
            
        Returns:
            Dictionary with verification status and optional token
        """
        from app.core.security import create_access_token
        
        # Find most recent non-expired, non-verified OTP
        otp_token = db.query(OTPToken).filter(
            OTPToken.phone_or_email == phone_or_email,
            OTPToken.verified == False,
            OTPToken.expires_at > datetime.utcnow()
        ).order_by(OTPToken.created_at.desc()).first()
        
        if not otp_token:
            return {"success": False, "message": "No valid OTP found or OTP expired", "token": None}
        
        # Check attempts
        if otp_token.attempts >= 3:
            return {"success": False, "message": "Too many failed attempts. Request a new OTP.", "token": None}
        
        # Verify OTP
        if verify_otp(otp, otp_token.token_hash):
            # Mark as verified
            otp_token.verified = True
            otp_token.verified_at = datetime.utcnow()
            
            # Mark reporter as verified if linked
            if otp_token.reporter_id:
                reporter = db.query(Reporter).filter(Reporter.id == otp_token.reporter_id).first()
                if reporter:
                    reporter.verified = True
            
            db.commit()
            
            # Generate access token
            token_data = {
                "reporter_id": otp_token.reporter_id,
                "phone_or_email": phone_or_email,
                "verified": True
            }
            access_token = create_access_token(token_data)
            
            logger.info(f"OTP verified successfully for {phone_or_email}")
            return {"success": True, "message": "OTP verified successfully", "token": access_token}
        else:
            # Increment attempts
            otp_token.attempts += 1
            db.commit()
            
            remaining = 3 - otp_token.attempts
            return {
                "success": False,
                "message": f"Invalid OTP. {remaining} attempts remaining.",
                "token": None
            }


# Export singleton instance
otp_service = OTPService()
