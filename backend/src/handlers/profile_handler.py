"""Profile management API handlers"""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from pydantic import BaseModel, Field

from src.middleware.auth_middleware import get_current_user
from src.services.profile_service import ProfileService
from src.models.user import StudentProfile, ProfileUpdate
from src.utils.errors import (
    ValidationError,
    NotFoundError,
    error_response,
    success_response
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profile", tags=["profile"])
profile_service = ProfileService()


class ProfileResponse(BaseModel):
    """Profile response model"""
    success: bool = True
    data: Optional[StudentProfile] = None
    message: Optional[str] = None


class ResumeUploadResponse(BaseModel):
    """Resume upload response model"""
    success: bool = True
    data: Optional[dict] = Field(None, description="Contains resumeUrl and extractedSkills")
    message: Optional[str] = None


@router.get("", response_model=ProfileResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user's profile
    
    Returns:
        ProfileResponse with user profile data
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Fetching profile for user: {user_id}")
        
        profile = await profile_service.get_profile(user_id)
        
        if not profile:
            logger.warning(f"Profile not found for user: {user_id}")
            raise NotFoundError("Profile", user_id)
        
        logger.info(f"Profile retrieved successfully for user: {user_id}")
        return ProfileResponse(data=profile)
    
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching profile for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching profile"
        )


@router.put("", response_model=ProfileResponse)
async def update_profile(
    profile_update: ProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user's profile
    
    Args:
        profile_update: Profile fields to update
        
    Returns:
        ProfileResponse with updated profile data
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Updating profile for user: {user_id}")
        
        updated_profile = await profile_service.update_profile(user_id, profile_update)
        
        logger.info(f"Profile updated successfully for user: {user_id}")
        return ProfileResponse(
            data=updated_profile,
            message="Profile updated successfully"
        )
    
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating profile for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating profile"
        )


@router.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload resume and extract skills using AI
    
    Args:
        file: Resume file (PDF, DOCX, or TXT, max 10MB)
        
    Returns:
        ResumeUploadResponse with resume URL and extracted skills
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Resume upload attempt for user: {user_id}, file: {file.filename}")
        
        # Validate file type
        allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
        if file.content_type not in allowed_types:
            logger.warning(f"Invalid file type for user {user_id}: {file.content_type}")
            raise ValidationError(
                "Invalid file type. Only PDF, DOCX, and TXT files are allowed",
                details={"content_type": file.content_type, "allowed_types": allowed_types}
            )
        
        # Validate file size (10MB max)
        file_content = await file.read()
        file_size_mb = len(file_content) / (1024 * 1024)
        if len(file_content) > 10 * 1024 * 1024:
            logger.warning(f"File size exceeds limit for user {user_id}: {file_size_mb:.2f}MB")
            raise ValidationError(
                "File size exceeds 10MB limit",
                details={"file_size_mb": round(file_size_mb, 2), "max_size_mb": 10}
            )
        
        # Reset file pointer
        await file.seek(0)
        
        # Upload resume and extract skills
        logger.info(f"Processing resume for user {user_id}, size: {file_size_mb:.2f}MB")
        result = await profile_service.upload_resume(user_id, file, file_content)
        
        logger.info(f"Resume uploaded successfully for user {user_id}, extracted {len(result.get('extractedSkills', []))} skills")
        return ResumeUploadResponse(
            data=result,
            message="Resume uploaded and skills extracted successfully"
        )
    
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error uploading resume for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while uploading resume"
        )


@router.delete("", response_model=ProfileResponse)
async def delete_profile(current_user: dict = Depends(get_current_user)):
    """
    Delete current user's profile
    
    Returns:
        ProfileResponse with success message
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Deleting profile for user: {user_id}")
        
        await profile_service.delete_profile(user_id)
        
        logger.info(f"Profile deleted successfully for user: {user_id}")
        return ProfileResponse(
            data=None,
            message="Profile deleted successfully"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error deleting profile for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting profile"
        )
