"""Skill and skill graph models"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SkillStatus(str, Enum):
    """Skill verification status"""
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"


class SkillCategory(str, Enum):
    """Skill category"""
    PROGRAMMING_LANGUAGE = "programming_language"
    FRAMEWORK = "framework"
    TOOL = "tool"
    SOFT_SKILL = "soft_skill"
    DOMAIN_KNOWLEDGE = "domain_knowledge"


class SkillSource(str, Enum):
    """Source of skill"""
    RESUME = "resume"
    PROJECT = "project"
    VALIDATION = "validation"
    MANUAL = "manual"


class SkillNode(BaseModel):
    """Individual skill node"""
    skill_id: str = Field(alias="skillId")
    name: str
    normalized_name: str = Field(alias="normalizedName")
    category: SkillCategory
    status: SkillStatus
    proficiency_level: int = Field(alias="proficiencyLevel", ge=0, le=100)
    verified: bool = False
    verified_at: Optional[str] = Field(None, alias="verifiedAt")
    validation_id: Optional[str] = Field(None, alias="validationId")
    source: SkillSource
    source_details: Optional[str] = Field(None, alias="sourceDetails")
    related_skills: list[str] = Field(default_factory=list, alias="relatedSkills")
    prerequisites: list[str] = Field(default_factory=list)
    added_at: str = Field(alias="addedAt")
    last_updated_at: str = Field(alias="lastUpdatedAt")

    class Config:
        populate_by_name = True


class SkillGraph(BaseModel):
    """Student's skill graph"""
    user_id: str = Field(alias="userId")
    skills: list[SkillNode] = []
    total_skills: int = Field(0, alias="totalSkills")
    verified_skills: int = Field(0, alias="verifiedSkills")
    in_progress_skills: int = Field(0, alias="inProgressSkills")
    last_updated: str = Field(alias="lastUpdated")

    class Config:
        populate_by_name = True


class SkillGap(BaseModel):
    """Skill gap for internship"""
    skill_name: str = Field(alias="skillName")
    required: bool
    current_proficiency: int = Field(alias="currentProficiency", ge=0, le=100)
    target_proficiency: int = Field(alias="targetProficiency", ge=0, le=100)
    priority: str  # "high" | "medium" | "low"

    class Config:
        populate_by_name = True
