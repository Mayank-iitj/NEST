"""AI service for OpenAI integration and pharmacovigilance automation."""
from openai import OpenAI
from app.core.config import settings
from typing import Dict, List, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class AIService:
    """AI service for pharmacovigilance automation."""
    
    @staticmethod
    def detect_missing_fields(event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze adverse event report and detect missing regulatory-relevant fields.
        
        Args:
            event_data: Dictionary containing event information
            
        Returns:
            Dictionary with required_fields, optional_fields, and risk_reasoning
        """
        prompt = f"""You are a pharmacovigilance data auditor analyzing adverse event reports.
        
Analyze this adverse event report and list missing regulatory-relevant fields:

EVENT DATA:
- Suspected drug: {event_data.get('suspected_drug', 'NOT PROVIDED')}
- Dose: {event_data.get('dose', 'NOT PROVIDED')}
- Frequency: {event_data.get('frequency', 'NOT PROVIDED')}
- Start date: {event_data.get('start_date', 'NOT PROVIDED')}
- Stop date: {event_data.get('stop_date', 'NOT PROVIDED')}
- Adverse effect: {event_data.get('adverse_effect', 'NOT PROVIDED')}
- Seriousness: {event_data.get('seriousness', 'NOT PROVIDED')}
- Hospitalization: {event_data.get('hospitalization', 'NOT PROVIDED')}
- Outcome: {event_data.get('outcome', 'NOT PROVIDED')}
- Comorbidities: {event_data.get('comorbidities', 'NOT PROVIDED')}
- Medications: {event_data.get('medications', 'NOT PROVIDED')}

Return ONLY valid JSON with this exact structure:
{{
  "required_fields": ["field1", "field2"],
  "optional_fields": ["field3", "field4"],
  "risk_reasoning": "Brief explanation of why missing fields matter for safety assessment"
}}

Focus on ICH E2B(R3) regulatory requirements."""
        
        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.OPENAI_TEMPERATURE,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            # Parse JSON from response
            result = json.loads(content)
            return result
            
        except Exception as e:
            logger.error(f"Error detecting missing fields: {str(e)}")
            return {
                "required_fields": [],
                "optional_fields": [],
                "risk_reasoning": "Error analyzing fields"
            }
    
    @staticmethod
    def generate_micro_followup(
        field_name: str,
        event_context: Dict[str, Any],
        language: str = "en",
        reporter_type: str = "patient"
    ) -> str:
        """
        Generate a single, 20-second micro follow-up question.
        
        Args:
            field_name: The missing field to ask about
            event_context: Context from the event
            language: Target language code
            reporter_type: 'patient' or 'hcp'
            
        Returns:
            Generated question text
        """
        language_names = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "ar": "Arabic",
            "hi": "Hindi",
            "zh": "Chinese",
            "pt": "Portuguese",
            "ru": "Russian",
            "de": "German"
        }
        
        lang_name = language_names.get(language, "English")
        audience = "patient in simple, non-medical language" if reporter_type == "patient" else "healthcare professional"
        
        prompt = f"""Generate a single, 20-second follow-up question for {audience} in {lang_name}.

CONTEXT:
- Missing field: {field_name}
- Suspected drug: {event_context.get('suspected_drug', 'medication')}
- Adverse effect: {event_context.get('adverse_effect', 'reaction')}

REQUIREMENTS:
- ONE question only
- Takes ≤20 seconds to answer
- Reassuring, trusted tone
- Non-threatening
- Add one scam-safety reassurance sentence
- Language: {lang_name}

Example format for English:
"Quick question about your medication report: [specific question]?

🛡️ This is secure — we never ask for payment or personal financial information."

Generate the question now:"""
        
        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,  # Slightly higher for creative questions
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating follow-up question: {str(e)}")
            return f"We need information about: {field_name}. Can you provide this detail?"
    
    @staticmethod
    def calculate_risk_score(event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate risk score and classification for an adverse event.
        
        Args:
            event_data: Dictionary containing event information
            
        Returns:
            Dictionary with score, hospitalization_risk, mortality_risk, class, reasoning
        """
        prompt = f"""You are a pharmacovigilance risk assessor. Analyze this adverse event and assign a severity score.

EVENT DATA:
- Suspected drug: {event_data.get('suspected_drug', 'unknown')}
- Adverse effect: {event_data.get('adverse_effect', 'unknown')}
- Seriousness: {event_data.get('seriousness', 'unknown')}
- Hospitalization: {event_data.get('hospitalization', 'unknown')}
- Outcome: {event_data.get('outcome', 'unknown')}
- Comorbidities: {event_data.get('comorbidities', 'unknown')}

Return ONLY valid JSON with this exact structure:
{{
  "score": 75,
  "hospitalization_risk": 0.45,
  "mortality_risk": 0.12,
  "class": "high",
  "reasoning": "Brief clinical reasoning for the risk assessment"
}}

SCORING RULES:
- score: 0-100 (0=minimal, 100=critical)
- hospitalization_risk: 0.0-1.0 probability
- mortality_risk: 0.0-1.0 probability
- class: "low" | "medium" | "high" | "critical"
  - low: score 0-25
  - medium: score 26-50
  - high: score 51-75
  - critical: score 76-100"""
        
        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.OPENAI_TEMPERATURE,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            result = json.loads(content)
            return result
            
        except Exception as e:
            logger.error(f"Error calculating risk score: {str(e)}")
            # Default conservative risk assessment
            return {
                "score": 50,
                "hospitalization_risk": 0.3,
                "mortality_risk": 0.1,
                "class": "medium",
                "reasoning": "Unable to complete automated assessment"
            }
    
    @staticmethod
    def generate_regulatory_summary(event_data: Dict[str, Any]) -> str:
        """
        Generate ICSR-ready regulatory narrative from structured data.
        
        Args:
            event_data: Complete event information
            
        Returns:
            Formatted regulatory narrative
        """
        prompt = f"""Convert this adverse event data into a formal pharmacovigilance narrative for regulatory submission (ICSR format).

EVENT DATA:
Reporter: {event_data.get('reporter_type', 'patient')}
Drug: {event_data.get('suspected_drug', 'unknown')}
Dose: {event_data.get('dose', 'unknown')}
Frequency: {event_data.get('frequency', 'unknown')}
Duration: {event_data.get('start_date', 'unknown')} to {event_data.get('stop_date', 'unknown')}
Adverse Effect: {event_data.get('adverse_effect', 'unknown')}
Seriousness: {event_data.get('seriousness', 'unknown')}
Hospitalization: {event_data.get('hospitalization', 'no')}
Outcome: {event_data.get('outcome', 'unknown')}
Comorbidities: {event_data.get('comorbidities', 'none reported')}
Concomitant Medications: {event_data.get('medications', 'none reported')}

Generate a professional, regulatory-compliant narrative following ICH E2B(R3) guidelines.
Use past tense, third person, and medical terminology.
Include all relevant safety information.
Be concise but complete (3-5 sentences)."""
        
        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.OPENAI_TEMPERATURE,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating regulatory summary: {str(e)}")
            return "Automated narrative generation unavailable. Manual review required."


# Export singleton instance
ai_service = AIService()
