"""Validation schemas and utilities using Pydantic"""

import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


# Password validation regex
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)

# GitHub URL regex
GITHUB_URL_REGEX = re.compile(
    r"^https?://github\.com/[\w-]+/[\w.-]+/?$"
)


class SignupSchema(BaseModel):
    """Signup request validation"""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    name: str = Field(min_length=1, max_length=100)
    
    @validator("password")
    def validate_password(cls, v):
        if not PASSWORD_REGEX.match(v):
            raise ValueError(
                "Password must contain at least 8 characters, "
                "including uppercase, lowercase, number, and special character"
            )
        return v
    
    @validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class SigninSchema(BaseModel):
    """Signin request validation"""
    email: EmailStr
    password: str = Field(min_length=1)


class RefreshTokenSchema(BaseModel):
    """Refresh token request validation"""
    refresh_token: str = Field(alias="refreshToken")
    
    class Config:
        populate_by_name = True


class ProfileUpdateSchema(BaseModel):
    """Profile update request validation"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, pattern=r"^(\+91)?[6-9]\d{9}$")
    location: Optional[str] = Field(None, max_length=100)
    linkedin_url: Optional[str] = Field(None, alias="linkedinUrl")
    github_username: Optional[str] = Field(None, alias="githubUsername", pattern=r"^[a-zA-Z0-9][a-zA-Z0-9-]{0,38}$")
    portfolio_url: Optional[str] = Field(None, alias="portfolioUrl")
    
    class Config:
        populate_by_name = True
    
    @validator("linkedin_url")
    def validate_linkedin_url(cls, v):
        if v and not v.startswith("https://linkedin.com/") and not v.startswith("https://www.linkedin.com/"):
            raise ValueError("Invalid LinkedIn URL")
        return v
    
    @validator("portfolio_url")
    def validate_portfolio_url(cls, v):
        if v and not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("Invalid portfolio URL")
        return v


class AddSkillSchema(BaseModel):
    """Add skill request validation"""
    skill_name: str = Field(alias="skillName", min_length=1, max_length=50)
    category: str  # SkillCategory enum value
    proficiency_level: Optional[int] = Field(0, alias="proficiencyLevel", ge=0, le=100)
    
    class Config:
        populate_by_name = True
    
    @validator("skill_name")
    def validate_skill_name(cls, v):
        if not v.strip():
            raise ValueError("Skill name cannot be empty")
        return v.strip()
    
    @validator("category")
    def validate_category(cls, v):
        valid_categories = [
            "programming_language",
            "framework",
            "tool",
            "soft_skill",
            "domain_knowledge"
        ]
        if v not in valid_categories:
            raise ValueError(f"Invalid category. Must be one of: {', '.join(valid_categories)}")
        return v


class ProjectGenerationSchema(BaseModel):
    """Project generation request validation"""
    target_skills: list[str] = Field(alias="targetSkills", min_items=1, max_items=10)
    student_level: str = Field(alias="studentLevel")
    time_commitment: Optional[str] = Field(None, alias="timeCommitment")
    preferences: Optional[dict] = None
    
    class Config:
        populate_by_name = True
    
    @validator("target_skills")
    def validate_target_skills(cls, v):
        if not v:
            raise ValueError("At least one target skill is required")
        # Remove duplicates and empty strings
        cleaned = list(set(skill.strip() for skill in v if skill.strip()))
        if not cleaned:
            raise ValueError("At least one valid target skill is required")
        return cleaned
    
    @validator("student_level")
    def validate_student_level(cls, v):
        valid_levels = ["beginner", "intermediate", "advanced"]
        if v not in valid_levels:
            raise ValueError(f"Invalid student level. Must be one of: {', '.join(valid_levels)}")
        return v


class GitHubSubmissionSchema(BaseModel):
    """GitHub submission validation"""
    project_id: str = Field(alias="projectId")
    github_repo_url: str = Field(alias="githubRepoUrl")
    description: Optional[str] = None
    additional_notes: Optional[str] = Field(None, alias="additionalNotes")
    
    class Config:
        populate_by_name = True
    
    @validator("github_repo_url")
    def validate_github_url(cls, v):
        if not GITHUB_URL_REGEX.match(v):
            raise ValueError("Invalid GitHub repository URL")
        return v


class InternshipFilterSchema(BaseModel):
    """Internship filter parameters"""
    type: Optional[str] = None  # "remote" | "onsite" | "hybrid"
    location: Optional[str] = None
    min_stipend: Optional[float] = Field(None, alias="minStipend", ge=0)
    
    class Config:
        populate_by_name = True
    
    @validator("type")
    def validate_type(cls, v):
        if v and v not in ["remote", "onsite", "hybrid"]:
            raise ValueError("Invalid type. Must be one of: remote, onsite, hybrid")
        return v


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address
        
    Returns:
        True if valid
    """
    email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return bool(email_regex.match(email))


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    
    Args:
        password: Password string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[@$!%*?&]", password):
        return False, "Password must contain at least one special character (@$!%*?&)"
    
    return True, ""


def validate_github_url(url: str) -> bool:
    """
    Validate GitHub repository URL
    
    Args:
        url: GitHub URL
        
    Returns:
        True if valid
    """
    return bool(GITHUB_URL_REGEX.match(url))


def normalize_skill_name(skill_name: str) -> str:
    """
    Normalize skill name for consistent storage
    
    Args:
        skill_name: Original skill name
        
    Returns:
        Normalized skill name (lowercase, no extra spaces)
    """
    return skill_name.strip().lower().replace("  ", " ")
