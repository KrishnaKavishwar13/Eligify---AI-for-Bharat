"""User and authentication models"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """User role enumeration"""
    STUDENT = "student"
    ADMIN = "admin"


class PersonalInfo(BaseModel):
    """Personal information"""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = Field(None, alias="linkedinUrl")
    github_username: Optional[str] = Field(None, alias="githubUsername")
    portfolio_url: Optional[str] = Field(None, alias="portfolioUrl")

    class Config:
        populate_by_name = True


class Education(BaseModel):
    """Education entry"""
    institution: str
    degree: str
    field: str
    start_date: str = Field(alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    cgpa: Optional[float] = None
    current: bool = False

    class Config:
        populate_by_name = True


class Experience(BaseModel):
    """Work experience entry"""
    company: str
    role: str
    description: str
    start_date: str = Field(alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    current: bool = False
    skills: list[str] = []

    class Config:
        populate_by_name = True


class ProjectEntry(BaseModel):
    """Project entry in profile"""
    project_id: str = Field(alias="projectId")
    title: str
    description: str
    github_url: Optional[str] = Field(None, alias="githubUrl")
    live_url: Optional[str] = Field(None, alias="liveUrl")
    skills: list[str] = []
    validated: bool = False

    class Config:
        populate_by_name = True


class Certification(BaseModel):
    """Certification entry"""
    name: str
    issuer: str
    issue_date: str = Field(alias="issueDate")
    expiry_date: Optional[str] = Field(None, alias="expiryDate")
    credential_url: Optional[str] = Field(None, alias="credentialUrl")

    class Config:
        populate_by_name = True


class StudentProfile(BaseModel):
    """Complete student profile"""
    user_id: str = Field(alias="userId")
    personal_info: PersonalInfo = Field(alias="personalInfo")
    education: list[Education] = []
    experience: list[Experience] = []
    projects: list[ProjectEntry] = []
    certifications: list[Certification] = []
    resume_s3_uri: Optional[str] = Field(None, alias="resumeS3Uri")
    resume_uploaded_at: Optional[str] = Field(None, alias="resumeUploadedAt")
    role: UserRole = UserRole.STUDENT
    onboarding_complete: bool = Field(False, alias="onboardingComplete")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    last_login_at: Optional[str] = Field(None, alias="lastLoginAt")

    class Config:
        populate_by_name = True


class AuthResult(BaseModel):
    """Authentication result"""
    success: bool
    user_id: Optional[str] = Field(None, alias="userId")
    access_token: Optional[str] = Field(None, alias="accessToken")
    refresh_token: Optional[str] = Field(None, alias="refreshToken")
    id_token: Optional[str] = Field(None, alias="idToken")
    error: Optional[str] = None

    class Config:
        populate_by_name = True


class TokenValidation(BaseModel):
    """Token validation result"""
    valid: bool
    user_id: Optional[str] = Field(None, alias="userId")
    role: Optional[UserRole] = None
    expires_at: Optional[int] = Field(None, alias="expiresAt")

    class Config:
        populate_by_name = True


class ProfileUpdate(BaseModel):
    """Profile update model with optional fields"""
    personal_info: Optional[PersonalInfo] = Field(None, alias="personalInfo")
    education: Optional[list[Education]] = None
    experience: Optional[list[Experience]] = None
    projects: Optional[list[ProjectEntry]] = None
    certifications: Optional[list[Certification]] = None
    onboarding_complete: Optional[bool] = Field(None, alias="onboardingComplete")

    class Config:
        populate_by_name = True
