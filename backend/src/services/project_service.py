"""Project generation and management service"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4

from src.config.settings import settings
from src.models.project import GeneratedProject, Milestone, ValidationCriterion, ProjectStatus
from src.utils.dynamodb import get_item, put_item, update_item, query_items
from src.utils.mock_store import mock_store
from src.services.ai_service import ai_service


class ProjectService:
    """Service for AI project generation and management"""
    
    @staticmethod
    async def generate_project(
        user_id: str,
        target_skills: List[str],
        student_level: str,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Optional[GeneratedProject]:
        """Generate project using AI"""
        
        # Get user context
        user_context = None
        
        # Generate project with AI
        ai_result = await ai_service.generate_project(
            target_skills, student_level, user_context
        )
        
        if not ai_result:
            return None
        
        now = datetime.utcnow().isoformat()
        project_id = str(uuid4())
        
        # Create validation criteria (weights must sum to 100)
        validation_criteria = [
            ValidationCriterion(
                criterionId=str(uuid4()),
                criterion="Code quality and best practices",
                weight=30,
                checkType="ai"
            ),
            ValidationCriterion(
                criterionId=str(uuid4()),
                criterion="Feature completeness",
                weight=40,
                checkType="ai"
            ),
            ValidationCriterion(
                criterionId=str(uuid4()),
                criterion="Documentation quality",
                weight=30,
                checkType="ai"
            )
        ]
        
        # Parse milestones
        milestones = []
        for idx, m in enumerate(ai_result.get("milestones", []), 1):
            milestone = Milestone(
                milestoneId=str(uuid4()),
                title=m.get("title", f"Milestone {idx}"),
                description=m.get("description", ""),
                tasks=m.get("tasks", []),
                estimatedHours=m.get("estimatedHours", 4),
                order=idx
            )
            milestones.append(milestone)
        
        project = GeneratedProject(
            projectId=project_id,
            userId=user_id,
            generatedFor="skill_gap",
            title=ai_result.get("title", "Learning Project"),
            description=ai_result.get("description", ""),
            objectives=ai_result.get("objectives", []),
            targetSkills=target_skills,
            skillsToLearn=target_skills,
            techStack=ai_result.get("techStack", []),
            milestones=milestones,
            validationCriteria=validation_criteria,
            resources=ai_result.get("resources", []),
            difficulty=student_level,
            estimatedDuration=ai_result.get("estimatedDuration", "1-2 weeks"),
            status="suggested",
            createdAt=now,
            updatedAt=now
        )
        
        # Save to mock store
        mock_store.save_project(project.dict(by_alias=True))
        return project
    
    @staticmethod
    async def get_project(project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID from mock store"""
        return mock_store.get_project(project_id)
    
    @staticmethod
    async def get_user_projects(user_id: str, status_filter: Optional[ProjectStatus] = None) -> List[Dict[str, Any]]:
        """List user's projects from mock store"""
        all_projects = mock_store.get_user_projects(user_id)
        
        if status_filter:
            return [p for p in all_projects if p.get("status") == status_filter.value]
        
        return all_projects
    
    @staticmethod
    async def update_project_status(project_id: str, new_status: ProjectStatus) -> Dict[str, Any]:
        """Update project status"""
        project = mock_store.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        
        now = datetime.utcnow().isoformat()
        project["status"] = new_status.value
        project["updatedAt"] = now
        
        if new_status == ProjectStatus.COMPLETED:
            project["completedAt"] = now
        elif new_status == ProjectStatus.IN_PROGRESS and "acceptedAt" not in project:
            project["acceptedAt"] = now
        
        mock_store.save_project(project)
        return project
    
    @staticmethod
    async def complete_project(user_id: str, project_id: str) -> Dict[str, Any]:
        """
        Mark project as complete and verify skills
        
        This method delegates to verification_service to handle:
        - Updating project status
        - Verifying skills
        - Re-classifying internships
        - Detecting eligibility changes
        """
        # Import here to avoid circular dependency
        from src.services.verification_service import verification_service
        
        return await verification_service.verify_project_completion(user_id, project_id)


project_service = ProjectService()
