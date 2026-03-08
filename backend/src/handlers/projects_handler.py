"""Project generation and management API handlers"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from src.middleware.auth_middleware import get_current_user
from src.services.project_service import ProjectService
from src.models.project import GeneratedProject, ProjectStatus
from src.utils.errors import (
    ValidationError,
    NotFoundError,
    ForbiddenError,
    AIServiceError,
    error_response,
    success_response
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projects", tags=["projects"])
project_service = ProjectService()


class GenerateProjectRequest(BaseModel):
    """Request model for project generation"""
    target_skills: List[str] = Field(..., min_items=1, max_items=10)
    student_level: str = Field(..., description="beginner, intermediate, or advanced")
    time_commitment: Optional[str] = Field(None, description="e.g., '2 weeks', '1 month'")


class ProjectResponse(BaseModel):
    """Single project response model"""
    success: bool = True
    data: Optional[GeneratedProject] = None
    message: Optional[str] = None


class ProjectsListResponse(BaseModel):
    """Projects list response model"""
    success: bool = True
    data: Optional[List[GeneratedProject]] = None
    message: Optional[str] = None


class ProjectCompletionResponse(BaseModel):
    """Project completion response model"""
    success: bool = True
    data: Optional[dict] = Field(None, description="Contains updated skill graph and newly eligible internships")
    message: Optional[str] = None


@router.post("/generate", response_model=ProjectResponse)
async def generate_project(
    request: GenerateProjectRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate AI-powered project roadmap for target skills
    
    Args:
        request: Target skills, student level, and time commitment
        
    Returns:
        ProjectResponse with generated project
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Generating project for user {user_id}, skills: {request.target_skills}, level: {request.student_level}")
        
        # Validate student level
        valid_levels = ["beginner", "intermediate", "advanced"]
        if request.student_level.lower() not in valid_levels:
            raise ValidationError(
                f"Invalid student level. Must be one of: {', '.join(valid_levels)}",
                details={"provided": request.student_level, "valid_levels": valid_levels}
            )
        
        # Generate project using AI service
        project = await project_service.generate_project(
            user_id=user_id,
            target_skills=request.target_skills,
            student_level=request.student_level,
            time_commitment=request.time_commitment
        )
        
        if not project:
            logger.error(f"AI service failed to generate project for user {user_id}")
            raise AIServiceError("Failed to generate project. Please try again.")
        
        logger.info(f"Project generated successfully for user {user_id}: {project.get('title', 'Untitled')}")
        return ProjectResponse(
            data=project,
            message="Project generated successfully"
        )
    
    except (ValidationError, AIServiceError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating project for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating project"
        )


@router.get("", response_model=ProjectsListResponse)
async def list_projects(
    status_filter: Optional[ProjectStatus] = Query(None, alias="status", description="Filter by status"),
    current_user: dict = Depends(get_current_user)
):
    """
    List user's projects with optional status filter
    
    Query Parameters:
        - status: Filter by project status (suggested, in_progress, completed)
        
    Returns:
        ProjectsListResponse with list of projects
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Listing projects for user {user_id}, status filter: {status_filter}")
        
        # Get user's projects
        projects = await project_service.get_user_projects(user_id, status_filter)
        
        logger.info(f"Found {len(projects)} projects for user {user_id}")
        return ProjectsListResponse(
            data=projects,
            message=f"Found {len(projects)} projects"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error listing projects for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching projects"
        )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get specific project details
    
    Args:
        project_id: Project identifier
        
    Returns:
        ProjectResponse with project details
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Fetching project {project_id} for user {user_id}")
        
        # Get project
        project = await project_service.get_project(project_id)
        
        if not project:
            logger.warning(f"Project {project_id} not found")
            raise NotFoundError("Project", project_id)
        
        # Verify ownership
        if project.get("userId") != user_id:
            logger.warning(f"User {user_id} attempted to access project {project_id} owned by {project.get('userId')}")
            raise ForbiddenError("You don't have permission to access this project")
        
        logger.info(f"Project {project_id} retrieved successfully for user {user_id}")
        return ProjectResponse(data=project)
    
    except (NotFoundError, ForbiddenError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching project {project_id} for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching project"
        )


@router.put("/{project_id}/status", response_model=ProjectResponse)
async def update_project_status_endpoint(
    project_id: str,
    new_status: ProjectStatus,
    current_user: dict = Depends(get_current_user)
):
    """
    Update project status
    
    Args:
        project_id: Project identifier
        new_status: New status (suggested, in_progress, completed)
        
    Returns:
        ProjectResponse with updated project
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Updating project {project_id} status to {new_status} for user {user_id}")
        
        # Get project to verify ownership
        project = await project_service.get_project(project_id)
        
        if not project:
            logger.warning(f"Project {project_id} not found")
            raise NotFoundError("Project", project_id)
        
        if project.get("userId") != user_id:
            logger.warning(f"User {user_id} attempted to update project {project_id} owned by {project.get('userId')}")
            raise ForbiddenError("You don't have permission to update this project")
        
        # Update status
        updated_project = await project_service.update_project_status(project_id, new_status)
        
        logger.info(f"Project {project_id} status updated to {new_status} for user {user_id}")
        return ProjectResponse(
            data=updated_project,
            message=f"Project status updated to {new_status.value}"
        )
    
    except (NotFoundError, ForbiddenError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating project {project_id} status for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating project status"
        )


@router.post("/{project_id}/complete", response_model=ProjectCompletionResponse)
async def complete_project(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Mark project as complete and verify skills
    
    This will:
    1. Update project status to 'completed'
    2. Verify all target skills (set proficiency to 70, status to 'verified')
    3. Re-classify internships to find newly eligible opportunities
    
    Args:
        project_id: Project identifier
        
    Returns:
        ProjectCompletionResponse with updated skill graph and newly eligible internships
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Completing project {project_id} for user {user_id}")
        
        # Complete project and verify skills
        result = await project_service.complete_project(user_id, project_id)
        
        newly_eligible_count = len(result.get("newly_eligible_internships", []))
        logger.info(f"Project {project_id} completed for user {user_id}, {newly_eligible_count} newly eligible internships")
        
        return ProjectCompletionResponse(
            data=result,
            message="Project completed and skills verified successfully"
        )
    
    except (NotFoundError, ForbiddenError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error completing project {project_id} for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while completing project"
        )
