"""Follow-up routes for micro-questionnaires."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token, create_secure_link
from app.models.schemas import FollowupQuestionCreate, FollowupAnswerRequest, FollowupQuestionResponse
from app.models.database import Event, FollowupQuestion, AuditLog, Reporter
from app.services.ai_service import ai_service
from app.services.messaging_service import messaging_service
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/followup", tags=["Follow-up"])


@router.post("/send")
def send_followup_question(event_id: int, db: Session = Depends(get_db)):
    """
    Generate and send micro follow-up questions for missing fields.
    
    Automatically generates contextual questions based on missing fields.
    """
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        if not event.missing_fields or len(event.missing_fields) == 0:
            return {"message": "No missing fields detected", "questions_sent": 0}
        
        reporter = event.reporter
        if not reporter:
            raise HTTPException(status_code=400, detail="No reporter associated with event")
        
        # Get first missing field
        field_name = event.missing_fields[0]
        
        # Prepare event context
        event_context = {
            "suspected_drug": event.suspected_drug,
            "adverse_effect": event.adverse_effect
        }
        
        # Generate question using AI
        question_text = ai_service.generate_micro_followup(
            field_name=field_name,
            event_context=event_context,
            language=reporter.language,
            reporter_type=reporter.reporter_type
        )
        
        # Create secure link for answering
        secure_token = create_secure_link(reporter.id, event.id)
        secure_link = f"http://localhost:3000/answer?token={secure_token}"
        
        # Store question in database
        question = FollowupQuestion(
            event_id=event.id,
            question_text=question_text,
            field_name=field_name,
            question_language=reporter.language,
            channel=reporter.phone if reporter.phone else "email"
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        
        # Send via messaging service
        channel = "whatsapp" if reporter.phone else "email"
        contact = reporter.phone if reporter.phone else reporter.email
        
        success = messaging_service.send_followup_question(
            to=contact,
            question=question_text,
            channel=channel,
            secure_link=secure_link
        )
        
        # Update event status
        event.followup_status = "in_progress"
        db.commit()
        
        # Log audit trail
        audit = AuditLog(
            event_id=event.id,
            reporter_id=reporter.id,
            action="FOLLOWUP_SENT",
            channel=channel,
            meta={
                "field_name": field_name,
                "question_id": question.id,
                "success": success
            }
        )
        db.add(audit)
        db.commit()
        
        logger.info(f"Follow-up question sent for event {event_id}, field: {field_name}")
        
        return {
            "message": "Follow-up question sent",
            "question_id": question.id,
            "field_name": field_name,
            "channel": channel,
            "success": success
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending follow-up question: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send follow-up question")


@router.post("/answer")
def answer_followup_question(request: FollowupAnswerRequest, db: Session = Depends(get_db)):
    """
    Submit answer to a follow-up question.
    
    Requires valid token from secure link.
    """
    try:
        # Verify token
        payload = verify_token(request.token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # Get question
        question = db.query(FollowupQuestion).filter(
            FollowupQuestion.id == request.question_id
        ).first()
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        if question.answered:
            raise HTTPException(status_code=400, detail="Question already answered")
        
        # Update question with answer
        question.answered = True
        question.answer_text = request.answer_text
        question.answered_at = datetime.utcnow()
        
        # Update event with answered field
        event = question.event
        if event and question.field_name:
            # Set the field value on the event
            setattr(event, question.field_name, request.answer_text)
            
            # Remove from missing fields
            if event.missing_fields and question.field_name in event.missing_fields:
                event.missing_fields.remove(question.field_name)
            
            # Recalculate risk if needed
            from app.services.risk_service import risk_service
            risk_service.calculate_and_update_risk(db, event.id)
        
        db.commit()
        
        # Log audit trail
        audit = AuditLog(
            event_id=event.id if event else None,
            action="FOLLOWUP_ANSWERED",
            meta={
                "question_id": question.id,
                "field_name": question.field_name
            }
        )
        db.add(audit)
        db.commit()
        
        logger.info(f"Follow-up question {question.id} answered")
        
        return {
            "success": True,
            "message": "Answer submitted successfully",
            "question_id": question.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error answering follow-up question: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to submit answer")


@router.get("/questions/{event_id}", response_model=List[FollowupQuestionResponse])
def get_event_questions(event_id: int, db: Session = Depends(get_db)):
    """Get all follow-up questions for an event."""
    questions = db.query(FollowupQuestion).filter(
        FollowupQuestion.event_id == event_id
    ).order_by(FollowupQuestion.sent_at.desc()).all()
    
    return questions
