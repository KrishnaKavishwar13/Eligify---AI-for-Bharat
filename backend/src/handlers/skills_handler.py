"""Skill graph management API handlers"""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.middleware.auth_middleware import get_current_user
from src.services.skill_service import SkillService
from src.models.skill import SkillGraph, SkillNode, SkillCategory, SkillStatus
from src.utils.mock_store import mock_store
from src.utils.errors import (
    ValidationError,
    NotFoundError,
    error_response,
    success_response
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/skills", tags=["skills"])
skill_service = SkillService()


class SkillGraphResponse(BaseModel):
    """Skill graph response model"""
    success: bool = True
    data: Optional[SkillGraph] = None
    message: Optional[str] = None


class AddSkillRequest(BaseModel):
    """Request model for adding a skill"""
    skill_name: str = Field(..., min_length=1, max_length=100)
    category: SkillCategory


class AddSkillResponse(BaseModel):
    """Response model for adding a skill"""
    success: bool = True
    data: Optional[SkillNode] = None
    message: Optional[str] = None


class UpdateSkillRequest(BaseModel):
    """Request model for updating a skill"""
    status: Optional[SkillStatus] = None
    proficiency: Optional[int] = Field(None, ge=0, le=100)


@router.get("", response_model=None)
async def get_skill_graph(current_user: dict = Depends(get_current_user)):
    """
    Get current user's skill graph
    
    Returns:
        SkillGraphResponse with skill graph data
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Fetching skill graph for user: {user_id}")
        
        skill_graph_dict = mock_store.get_skill_graph(user_id)
        
        if not skill_graph_dict:
            logger.warning(f"Skill graph not found for user: {user_id}")
            raise NotFoundError("Skill graph", user_id)
        
        logger.info(f"Skill graph retrieved successfully for user: {user_id}")
        return {
            "success": True,
            "data": skill_graph_dict
        }
    
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching skill graph for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching skill graph"
        )


@router.post("", response_model=AddSkillResponse)
async def add_skill(
    skill_request: AddSkillRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Manually add a skill to user's skill graph
    
    Args:
        skill_request: Skill name and category
        
    Returns:
        AddSkillResponse with newly added skill
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Adding skill '{skill_request.skill_name}' for user: {user_id}")
        
        # Add skill to skill graph
        skill_node = await skill_service.add_skill(
            user_id,
            skill_request.skill_name,
            skill_request.category
        )
        
        logger.info(f"Skill '{skill_request.skill_name}' added successfully for user: {user_id}")
        return AddSkillResponse(
            data=skill_node,
            message="Skill added successfully"
        )
    
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error adding skill for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while adding skill"
        )


@router.put("/{skill_id}", response_model=SkillGraphResponse)
async def update_skill(
    skill_id: str,
    skill_update: UpdateSkillRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a skill's status or proficiency
    
    Args:
        skill_id: Skill identifier
        skill_update: Fields to update
        
    Returns:
        SkillGraphResponse with updated skill graph
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Updating skill '{skill_id}' for user: {user_id}")
        
        # Update skill status if provided
        if skill_update.status:
            await skill_service.update_skill_status(user_id, skill_id, skill_update.status)
        
        # Get updated skill graph
        skill_graph = await skill_service.get_skill_graph(user_id)
        
        logger.info(f"Skill '{skill_id}' updated successfully for user: {user_id}")
        return SkillGraphResponse(
            data=skill_graph,
            message="Skill updated successfully"
        )
    
    except ValidationError:
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating skill for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating skill"
        )
