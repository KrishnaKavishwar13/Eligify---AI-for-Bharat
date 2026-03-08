"""Internship models"""

from typing import Optional
from pydantic import BaseModel, Field


class RequiredSkill(BaseModel):
    """Required skill for internship"""
    name: str
    proficiency_level: int = Field(alias="proficiencyLevel", ge=0, le=100)
    mandatory: bool
    weight: float = 1.0  # Importance weight

    class Config:
        populate_by_name = True


class Stipend(BaseModel):
    """Stipend information"""
    amount: float
    currency: str = "INR"
    period: str  # "monthly" | "total"


class EligibilityCriteria(BaseModel):
    """Eligibility criteria for internship"""
    min_cgpa: Optional[float] = Field(None, alias="minCGPA")
    graduation_year: Optional[list[int]] = Field(None, alias="graduationYear")
    degrees: Optional[list[str]] = None
    institutions: Optional[list[str]] = None

    class Config:
        populate_by_name = True


class Internship(BaseModel):
    """Internship listing"""
    internship_id: str = Field(alias="internshipId")
    title: str
    company: str
    description: str
    required_skills: list[RequiredSkill] = Field(alias="requiredSkills")
    preferred_skills: list[str] = Field(default_factory=list, alias="preferredSkills")
    duration: str
    stipend: Optional[Stipend] = None
    location: str
    type: str  # "remote" | "onsite" | "hybrid"
    application_deadline: str = Field(alias="applicationDeadline")
    start_date: str = Field(alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    eligibility_criteria: Optional[EligibilityCriteria] = Field(None, alias="eligibilityCriteria")
    application_url: Optional[str] = Field(None, alias="applicationUrl")
    application_process: Optional[str] = Field(None, alias="applicationProcess")
    status: str = "active"  # "active" | "closed" | "draft"
    posted_by: str = Field(alias="postedBy")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    view_count: int = Field(0, alias="viewCount")
    application_count: int = Field(0, alias="applicationCount")

    class Config:
        populate_by_name = True


class InternshipMatch(BaseModel):
    """Internship match result"""
    internship: Internship
    match_score: float = Field(alias="matchScore", ge=0, le=100)
    missing_skills: list = Field(default_factory=list, alias="missingSkills")
    matched_skills: list[str] = Field(default_factory=list, alias="matchedSkills")
    missing_mandatory_skills: int = Field(0, alias="missingMandatorySkills")
    recommendation: Optional[str] = None

    class Config:
        populate_by_name = True


class ClassifiedInternships(BaseModel):
    """Classified internships by eligibility"""
    eligible: list[InternshipMatch] = []
    almost_eligible: list[InternshipMatch] = Field(default_factory=list, alias="almostEligible")
    not_eligible: list[InternshipMatch] = Field(default_factory=list, alias="notEligible")

    class Config:
        populate_by_name = True
