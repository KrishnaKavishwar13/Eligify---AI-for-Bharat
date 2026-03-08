"""Pydantic models and types"""

from src.models.user import (
    UserRole,
    PersonalInfo,
    Education,
    Experience,
    ProjectEntry,
    Certification,
    StudentProfile,
    AuthResult,
    TokenValidation,
)
from src.models.skill import (
    SkillStatus,
    SkillCategory,
    SkillSource,
    SkillNode,
    SkillGraph,
    SkillGap,
)
from src.models.internship import (
    RequiredSkill,
    Stipend,
    EligibilityCriteria,
    Internship,
    InternshipMatch,
    ClassifiedInternships,
)
from src.models.project import (
    TechStackItem,
    Milestone,
    ValidationCriterion,
    Resource,
    GeneratedProject,
    ProjectGenerationRequest,
    ProjectSuggestion,
)

__all__ = [
    # User models
    "UserRole",
    "PersonalInfo",
    "Education",
    "Experience",
    "ProjectEntry",
    "Certification",
    "StudentProfile",
    "AuthResult",
    "TokenValidation",
    # Skill models
    "SkillStatus",
    "SkillCategory",
    "SkillSource",
    "SkillNode",
    "SkillGraph",
    "SkillGap",
    # Internship models
    "RequiredSkill",
    "Stipend",
    "EligibilityCriteria",
    "Internship",
    "InternshipMatch",
    "ClassifiedInternships",
    # Project models
    "TechStackItem",
    "Milestone",
    "ValidationCriterion",
    "Resource",
    "GeneratedProject",
    "ProjectGenerationRequest",
    "ProjectSuggestion",
]
