"""Messaging service for WhatsApp, SMS, and email communication."""
from app.core.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class MessagingService:
    """Unified messaging service for multi-channel communication."""
    
    def __init__(self):
        """Initialize messaging clients."""
        self.mock_mode = settings.WHATSAPP_API_KEY == "mock" or settings.TWILIO_ACCOUNT_SID == "mock"
        
        if not self.mock_mode:
            try:
                from twilio.rest import Client
                self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            except Exception as e:
                logger.warning(f"Failed to initialize Twilio client: {e}. Using mock mode.")
                self.mock_mode = True
    
    def send_message(self, to: str, message: str, channel: str = "sms") -> bool:
        """
        Send message via specified channel.
        
        Args:
            to: Phone number or email address
            message: Message content
            channel: 'sms', 'whatsapp', or 'email'
            
        Returns:
            True if sent successfully, False otherwise
        """
        if self.mock_mode:
            logger.info(f"[MOCK] Sending {channel} to {to}: {message[:50]}...")
            return True
        
        try:
            if channel == "sms":
                return self._send_sms(to, message)
            elif channel == "whatsapp":
                return self._send_whatsapp(to, message)
            elif channel == "email":
                return self._send_email(to, message)
            else:
                logger.error(f"Unknown channel: {channel}")
                return False
        except Exception as e:
            logger.error(f"Error sending message via {channel}: {str(e)}")
            return False
    
    def _send_sms(self, to: str, message: str) -> bool:
        """Send SMS via Twilio."""
        try:
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=to
            )
            logger.info(f"SMS sent successfully: {message_obj.sid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            return False
    
    def _send_whatsapp(self, to: str, message: str) -> bool:
        """Send WhatsApp message via Twilio or WhatsApp Cloud API."""
        try:
            # Ensure phone number has whatsapp: prefix for Twilio
            whatsapp_to = f"whatsapp:{to}" if not to.startswith("whatsapp:") else to
            whatsapp_from = f"whatsapp:{settings.TWILIO_PHONE_NUMBER}"
            
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=whatsapp_from,
                to=whatsapp_to
            )
            logger.info(f"WhatsApp sent successfully: {message_obj.sid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send WhatsApp: {str(e)}")
            return False
    
    def _send_email(self, to: str, message: str, subject: str = "Pharmacovigilance Follow-Up") -> bool:
        """Send email via SMTP."""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_USER
            msg['To'] = to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(settings.SMTP_USER, to, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {to}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_followup_question(
        self,
        to: str,
        question: str,
        channel: str,
        secure_link: Optional[str] = None
    ) -> bool:
        """
        Send follow-up question with secure link.
        
        Args:
            to: Phone number or email
            question: Question text
            channel: Communication channel
            secure_link: Optional secure link for answering
            
        Returns:
            True if sent successfully
        """
        message = f"""🏥 [Verified Medical Sender]

{question}

"""
        
        if secure_link:
            message += f"Click here to answer: {secure_link}\n\n"
        
        message += """🛡️ Security reminder:
✅ We never ask for payment
✅ We never ask for passwords
❌ Do not share this link"""
        
        return self.send_message(to, message, channel)


# Export singleton instance
messaging_service = MessagingService()
