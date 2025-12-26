"""Security utilities for JWT, encryption, and RBAC."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from app.core.config import settings
import hashlib
import secrets
import base64

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Encryption cipher
def get_cipher():
    """Get Fernet cipher for AES-256 encryption."""
    # Ensure key is 32 bytes for Fernet
    key = settings.ENCRYPTION_KEY.encode()[:32]
    key_b64 = base64.urlsafe_b64encode(key.ljust(32, b'\0'))
    return Fernet(key_b64)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP."""
    return ''.join([str(secrets.randbelow(10)) for _ in range(length)])


def hash_otp(otp: str) -> str:
    """Hash OTP for secure storage."""
    return hashlib.sha256(otp.encode()).hexdigest()


def verify_otp(plain_otp: str, hashed_otp: str) -> bool:
    """Verify OTP against its hash."""
    return hash_otp(plain_otp) == hashed_otp


def encrypt_phi(data: str) -> bytes:
    """Encrypt Protected Health Information using AES-256."""
    cipher = get_cipher()
    return cipher.encrypt(data.encode())


def decrypt_phi(encrypted_data: bytes) -> str:
    """Decrypt Protected Health Information."""
    cipher = get_cipher()
    return cipher.decrypt(encrypted_data).decode()


def create_secure_link(reporter_id: int, event_id: Optional[int] = None) -> str:
    """Create a secure, time-limited link for follow-up."""
    data = {
        "reporter_id": reporter_id,
        "type": "followup",
    }
    if event_id:
        data["event_id"] = event_id
    
    # Short-lived token (15 minutes)
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    return token


# RBAC Roles
class Roles:
    PATIENT = "patient"
    HCP = "hcp"
    PV_OFFICER = "pharmacovigilance_officer"
    ADMIN = "admin"


def check_permission(user_role: str, required_roles: list) -> bool:
    """Check if user role has required permissions."""
    return user_role in required_roles
