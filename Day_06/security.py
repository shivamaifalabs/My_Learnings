# app/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta,timezone
from jose import jwt
import uuid
from app.config import settings
from typing import Dict, Any

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM if hasattr(settings, "ALGORITHM") else "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

# Password Hashing (protect against >72 bytes)
def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        password = password_bytes.decode("utf-8", errors="ignore")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_bytes = plain_password.encode("utf-8")
    if len(pw_bytes) > 72:
        pw_bytes = pw_bytes[:72]
        plain_password = pw_bytes.decode("utf-8", errors="ignore")
    return pwd_context.verify(plain_password, hashed_password)

# JWT helpers: exp stored as integer (unix timestamp)
def create_access_token(subject: Dict[str, Any], expires_minutes: int = None) -> str:
    to_encode = subject.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes if expires_minutes else ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": int(expire.timestamp()), "jti": jti})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_refresh_token(subject: Dict[str, Any], expires_days: int = None) -> str:
    to_encode = subject.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=expires_days if expires_days else REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": int(expire.timestamp()), "jti": jti})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> Dict[str, Any]:
    # will raise jose.JWTError (including ExpiredSignatureError) on invalid/expired tokens
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
