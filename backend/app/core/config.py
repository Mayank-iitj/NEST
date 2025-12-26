"""Core configuration and settings for the application."""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Pharmacovigilance System"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://pvuser:pvpass_secure_2024@localhost:5432/pharmacovigilance"
    
    # Redis
    REDIS_URL: str = "redis://:redis_secure_2024@localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ENCRYPTION_KEY: str = "32-byte-key-change-in-production-abcd1234"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OTP_EXPIRE_MINUTES: int = 15
    OTP_LENGTH: int = 6
    
    # AI
    OPENAI_API_KEY: str = "sk-your-openai-api-key"
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_TEMPERATURE: float = 0.3
    
    # Communication APIs
    WHATSAPP_API_KEY: str = "mock"
    TWILIO_ACCOUNT_SID: str = "mock"
    TWILIO_AUTH_TOKEN: str = "mock"
    TWILIO_PHONE_NUMBER: str = "+1234567890"
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Supported languages
    SUPPORTED_LANGUAGES: List[str] = ["en", "es", "fr", "ar", "hi", "zh", "pt", "ru", "de"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
