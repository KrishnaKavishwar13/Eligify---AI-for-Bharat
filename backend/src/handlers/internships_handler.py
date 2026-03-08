"""Internship management and eligibility API handlers"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from src.middleware.auth_middleware import get_current_user
from src.services.eligibility_service import EligibilityService
from src.models.internship import Internship, ClassifiedInternships
from src.utils.errors import (
    ValidationError,
    NotFoundError,
    error_response,
    success_response
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/internships", tags=["internships"])
eligibility_service = EligibilityService()


class InternshipsResponse(BaseModel):
    """Internships list response model"""
    success: bool = True
    data: Optional[List[Internship]] = None
    message: Optional[str] = None


class InternshipResponse(BaseModel):
    """Single internship response model"""
    success: bool = True
    data: Optional[Internship] = None
    message: Optional[str] = None


class ClassificationResponse(BaseModel):
    """Internship classification response model"""
    success: bool = True
    data: Optional[ClassifiedInternships] = None
    message: Optional[str] = None


class SkillGapsResponse(BaseModel):
    """Skill gaps response model"""
    success: bool = True
    data: Optional[dict] = None
    message: Optional[str] = None


@router.get("", response_model=InternshipsResponse)
async def list_internships(
    internship_type: Optional[str] = Query(None, description="Filter by type: remote, onsite, hybrid"),
    location: Optional[str] = Query(None, description="Filter by location"),
    min_stipend: Optional[int] = Query(None, description="Minimum stipend"),
    current_user: dict = Depends(get_current_user)
):
    """
    List all active internships with optional filters
    
    Query Parameters:
        - type: Filter by internship type (remote, onsite, hybrid)
        - location: Filter by location
        - min_stipend: Minimum stipend amount
        
    Returns:
        InternshipsResponse with list of internships
    """
    try:
        logger.info(f"Listing internships for user: {current_user['user_id']}, filters: type={internship_type}, location={location}, min_stipend={min_stipend}")
        
        from src.utils.mock_store import mock_store
        from src.models.internship import Internship
        
        # Get all internships
        internships_data = mock_store.get_all_internships()
        internships = [Internship(**i) for i in internships_data]
        
        # Apply filters
        if internship_type:
            internships = [i for i in internships if i.type.lower() == internship_type.lower()]
        
        if location:
            internships = [i for i in internships if location.lower() in i.location.lower()]
        
        if min_stipend and min_stipend > 0:
            internships = [i for i in internships if i.stipend and i.stipend.amount >= min_stipend]
        
        # Filter only active internships
        internships = [i for i in internships if i.status == "active"]
        
        logger.info(f"Found {len(internships)} internships matching filters")
        return InternshipsResponse(
            data=internships,
            message=f"Found {len(internships)} internships"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error listing internships for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching internships"
        )


@router.get("/classify")
async def classify_internships(current_user: dict = Depends(get_current_user)):
    """
    Classify all internships for current user into:
    - Eligible (score >= 80, no mandatory skills missing)
    - Almost Eligible (score >= 50, <= 2 mandatory skills missing)
    - Not Eligible (otherwise)
    
    Returns:
        ClassificationResponse with classified internships
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Classifying internships for user: {user_id}")
        
        # Import services
        from src.services.skill_service import skill_service
        from src.utils.mock_store import mock_store
        from src.models.internship import Internship
        
        # Get user's skill graph
        skill_graph = await skill_service.get_skill_graph(user_id)
        if not skill_graph:
            logger.warning(f"Skill graph not found for user: {user_id}")
            raise NotFoundError("Skill graph", user_id)
        
        # Get all internships - keep as dicts
        internships_data = mock_store.get_all_internships()
        
        # Classify using eligibility service (pass dicts, not Pydantic models)
        classification = eligibility_service.classify_internships_dict(skill_graph, internships_data)
        
        logger.info(f"Internships classified for user {user_id}: {len(classification['eligible'])} eligible, {len(classification['almostEligible'])} almost eligible, {len(classification['notEligible'])} not eligible")
        return {
            "success": True,
            "data": classification,
            "message": "Internships classified successfully"
        }
    
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error classifying internships for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while classifying internships"
        )


@router.get("/{internship_id}", response_model=InternshipResponse)
async def get_internship(
    internship_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get specific internship details
    
    Args:
        internship_id: Internship identifier
        
    Returns:
        InternshipResponse with internship details
    """
    try:
        logger.info(f"Fetching internship {internship_id} for user: {current_user['user_id']}")
        
        from src.utils.mock_store import mock_store
        from src.models.internship import Internship
        
        # Get internship from mock store
        internship_data = mock_store.get_internship(internship_id)
        
        if not internship_data:
            logger.warning(f"Internship {internship_id} not found")
            raise NotFoundError("Internship", internship_id)
        
        internship = Internship(**internship_data)
        
        logger.info(f"Internship {internship_id} retrieved successfully")
        return InternshipResponse(
            data=internship,
            message="Internship retrieved successfully"
        )
    
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching internship {internship_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching internship"
        )


@router.get("/skills/gaps", response_model=SkillGapsResponse)
async def get_skill_gaps(
    internship_id: str = Query(..., description="Internship ID to analyze"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get missing skills for a specific internship
    
    Query Parameters:
        - internship_id: Internship to analyze
        
    Returns:
        SkillGapsResponse with missing skills and proficiency gaps
    """
    try:
        user_id = current_user["user_id"]
        
        # TODO: Implement skill gap analysis
        # 1. Fetch user's skill graph
        # 2. Fetch internship requirements
        # 3. Calculate missing skills and proficiency gaps
        
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Skill gap analysis not yet implemented. TODO: Compare user skills with internship requirements"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze skill gaps: {str(e)}"
        )
