"""JWT authentication utilities"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config.settings import settings
from src.models.user import UserRole


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: str,
    role: UserRole,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    
    Args:
        user_id: User ID
        role: User role
        expires_delta: Optional custom expiration time
        
    Returns:
        JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "sub": user_id,
        "role": role.value,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    user_id: str,
    role: UserRole,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token
    
    Args:
        user_id: User ID
        role: User role
        expires_delta: Optional custom expiration time
        
    Returns:
        JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "sub": user_id,
        "role": role.value,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def generate_tokens(user_id: str, role: UserRole) -> Dict[str, str]:
    """
    Generate both access and refresh tokens
    
    Args:
        user_id: User ID
        role: User role
        
    Returns:
        Dictionary with access_token and refresh_token
    """
    access_token = create_access_token(user_id, role)
    refresh_token = create_refresh_token(user_id, role)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
        token_type: Expected token type ("access" or "refresh")
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Verify token type
        if payload.get("type") != token_type:
            return None
        
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            return None
        
        return payload
        
    except JWTError:
        return None


def extract_user_from_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Extract user information from token
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary with user_id and role, or None if invalid
    """
    payload = verify_token(token, token_type="access")
    
    if not payload:
        return None
    
    user_id = payload.get("sub")
    role = payload.get("role")
    exp = payload.get("exp")
    
    if not user_id or not role:
        return None
    
    return {
        "user_id": user_id,
        "role": UserRole(role),
        "expires_at": exp
    }


def decode_token_without_verification(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode token without verification (for debugging/logging only)
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded payload or None
    """
    try:
        return jwt.decode(
            token,
            options={"verify_signature": False, "verify_exp": False}
        )
    except JWTError:
        return None


def is_token_expired(token: str) -> bool:
    """
    Check if token is expired
    
    Args:
        token: JWT token string
        
    Returns:
        True if token is expired
    """
    payload = decode_token_without_verification(token)
    
    if not payload:
        return True
    
    exp = payload.get("exp")
    if not exp:
        return True
    
    return datetime.fromtimestamp(exp) < datetime.utcnow()


def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Get token expiration datetime
    
    Args:
        token: JWT token string
        
    Returns:
        Expiration datetime or None
    """
    payload = decode_token_without_verification(token)
    
    if not payload:
        return None
    
    exp = payload.get("exp")
    if not exp:
        return None
    
    return datetime.fromtimestamp(exp)
