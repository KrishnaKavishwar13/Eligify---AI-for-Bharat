"""Authentication API handlers"""

import logging
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ValidationError as PydanticValidationError

from src.services.auth_service import auth_service
from src.utils.validation import SignupSchema, SigninSchema, RefreshTokenSchema
from src.utils.errors import (
    ValidationError,
    UnauthorizedError,
    ConflictError,
    error_response,
    success_response
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


class SignupResponse(BaseModel):
    """Signup response"""
    success: bool
    user_id: str | None = None
    message: str


class UserInfo(BaseModel):
    """User information"""
    userId: str
    email: str
    name: str
    role: str


class SigninResponse(BaseModel):
    """Signin response"""
    success: bool
    user: UserInfo | None = None
    accessToken: str | None = None
    refreshToken: str | None = None
    idToken: str | None = None


class RefreshResponse(BaseModel):
    """Refresh token response"""
    success: bool
    access_token: str | None = None
    refresh_token: str | None = None


class SignoutResponse(BaseModel):
    """Signout response"""
    success: bool
    message: str


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(data: SignupSchema):
    """
    Register new user account
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters with uppercase, lowercase, number, and special character
    - **name**: Full name
    """
    try:
        logger.info(f"Signup attempt for email: {data.email}")
        
        result = await auth_service.sign_up(
            email=data.email,
            password=data.password,
            name=data.name
        )
        
        if not result.success:
            logger.warning(f"Signup failed for {data.email}: {result.error}")
            
            # Check if user already exists
            if result.error and "already exists" in result.error.lower():
                raise ConflictError(
                    "An account with this email already exists",
                    details={"email": data.email}
                )
            
            raise ValidationError(result.error or "Signup failed")
        
        logger.info(f"Signup successful for {data.email}, user_id: {result.user_id}")
        
        return SignupResponse(
            success=True,
            user_id=result.user_id,
            message="Account created successfully. Please check your email for verification." 
                    if result.user_id else "Verification email sent"
        )
    
    except (ValidationError, ConflictError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error during signup: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during signup"
        )


@router.post("/signin", response_model=SigninResponse)
async def signin(data: SigninSchema):
    """
    Authenticate user and receive tokens
    
    - **email**: User email
    - **password**: User password
    """
    try:
        logger.info(f"Signin attempt for email: {data.email}")
        
        result = await auth_service.sign_in(
            email=data.email,
            password=data.password
        )
        
        if not result.success:
            logger.warning(f"Signin failed for {data.email}: {result.error}")
            raise UnauthorizedError(result.error or "Invalid email or password")
        
        logger.info(f"Signin successful for {data.email}")
        
        # Get user info
        user_info = await auth_service.get_user_info(result.user_id)
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve user information"
            )
        
        return SigninResponse(
            success=True,
            user=UserInfo(
                userId=user_info["user_id"],
                email=user_info["email"],
                name=user_info["name"],
                role=user_info["role"]
            ),
            accessToken=result.access_token,
            refreshToken=result.refresh_token,
            idToken=result.id_token
        )
    
    except UnauthorizedError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during signin: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during signin"
        )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh(data: RefreshTokenSchema):
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Valid refresh token
    """
    try:
        logger.info("Token refresh attempt")
        
        result = await auth_service.refresh_token(data.refresh_token)
        
        if not result.success:
            logger.warning(f"Token refresh failed: {result.error}")
            raise UnauthorizedError(result.error or "Invalid or expired refresh token")
        
        logger.info("Token refresh successful")
        
        return RefreshResponse(
            success=True,
            access_token=result.access_token,
            refresh_token=result.refresh_token
        )
    
    except UnauthorizedError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during token refresh: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during token refresh"
        )


@router.post("/signout", response_model=SignoutResponse)
async def signout():
    """
    Sign out user (invalidate session)
    
    Note: Requires authentication header
    """
    try:
        logger.info("Signout attempt")
        
        # In production, extract user_id from JWT token
        # For now, just return success
        success = await auth_service.sign_out("user_id")
        
        logger.info("Signout successful")
        
        return SignoutResponse(
            success=success,
            message="Signed out successfully"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error during signout: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during signout"
        )


@router.get("/me")
async def get_current_user():
    """
    Get current user information
    
    Note: Requires authentication header
    This is a placeholder - will be implemented with auth middleware
    """
    return {
        "message": "This endpoint requires authentication middleware"
    }
