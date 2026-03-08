"""Project generation models"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    """Project status enumeration"""
    SUGGESTED = "suggested"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class TechStackItem(BaseModel):
    """Technology stack item"""
    category: str  # "frontend" | "backend" | "database" | "devops" | "other"
    technology: str
    version: Optional[str] = None
    purpose: str


class Milestone(BaseModel):
    """Project milestone"""
    milestone_id: str = Field(alias="milestoneId")
    title: str
    description: str
    tasks: list[str] = []
    estimated_hours: int = Field(alias="estimatedHours")
    order: int

    class Config:
        populate_by_name = True


class ValidationCriterion(BaseModel):
    """Validation criterion for project"""
    criterion_id: str = Field(alias="criterionId")
    criterion: str
    weight: int = Field(ge=0, le=100)
    check_type: str = Field(alias="checkType")  # "automated" | "manual" | "ai"
    check_details: Optional[str] = Field(None, alias="checkDetails")

    class Config:
        populate_by_name = True


class Resource(BaseModel):
    """Learning resource"""
    type: str  # "documentation" | "tutorial" | "video" | "article" | "tool"
    title: str
    url: str
    description: Optional[str] = None


class GeneratedProject(BaseModel):
    """AI-generated project"""
    project_id: str = Field(alias="projectId")
    user_id: str = Field(alias="userId")
    generated_for: str = Field(alias="generatedFor")  # "skill_gap" | "exploration" | "internship_prep"
    target_internship_id: Optional[str] = Field(None, alias="targetInternshipId")
    title: str
    description: str
    objectives: list[str] = []
    target_skills: list[str] = Field(alias="targetSkills")
    skills_to_learn: list[str] = Field(default_factory=list, alias="skillsToLearn")
    skills_to_reinforce: list[str] = Field(default_factory=list, alias="skillsToReinforce")
    tech_stack: list[TechStackItem] = Field(default_factory=list, alias="techStack")
    milestones: list[Milestone] = []
    validation_criteria: list[ValidationCriterion] = Field(default_factory=list, alias="validationCriteria")
    resources: list[Resource] = []
    difficulty: str  # "beginner" | "intermediate" | "advanced"
    estimated_duration: str = Field(alias="estimatedDuration")
    status: str = "suggested"  # "suggested" | "accepted" | "in_progress" | "submitted" | "completed"
    submission_id: Optional[str] = Field(None, alias="submissionId")
    github_repo_url: Optional[str] = Field(None, alias="githubRepoUrl")
    submitted_at: Optional[str] = Field(None, alias="submittedAt")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    accepted_at: Optional[str] = Field(None, alias="acceptedAt")
    completed_at: Optional[str] = Field(None, alias="completedAt")

    class Config:
        populate_by_name = True


class ProjectGenerationRequest(BaseModel):
    """Request to generate a project"""
    user_id: str = Field(alias="userId")
    target_skills: list[str] = Field(alias="targetSkills")
    student_level: str = Field(alias="studentLevel")  # "beginner" | "intermediate" | "advanced"
    time_commitment: Optional[str] = Field(None, alias="timeCommitment")
    preferences: Optional[dict] = None

    class Config:
        populate_by_name = True


class ProjectSuggestion(BaseModel):
    """Project suggestion with relevance"""
    project: GeneratedProject
    relevance_score: float = Field(alias="relevanceScore", ge=0, le=100)
    skills_addressed: list[str] = Field(alias="skillsAddressed")
    internships_unlocked: list[str] = Field(default_factory=list, alias="internshipsUnlocked")

    class Config:
        populate_by_name = True
