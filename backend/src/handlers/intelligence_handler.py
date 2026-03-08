"""Career Intelligence API handlers"""

import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from src.middleware.auth_middleware import get_current_user
from src.services.skill_gap_intelligence_service import SkillGapIntelligenceService
from src.services.internship_mapping_service import InternshipMappingService
from src.services.personalization_service import (
    personalization_service,
    PersonalizationContext,
    PersonalizedProjectSuggestion
)
from src.services.prediction_service import (
    prediction_service,
    SkillProgressPrediction,
    CareerReadinessPrediction
)
from src.services.skill_service import skill_service
from src.utils.errors import (
    ValidationError,
    NotFoundError,
    AIServiceError,
    error_response,
    success_response
)
from src.utils.validation import normalize_skill_name

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/intelligence", tags=["intelligence"])
skill_gap_service = SkillGapIntelligenceService()
internship_mapping_service = InternshipMappingService()


# Request/Response Models
class ProfileAnalysisRequest(BaseModel):
    """Request model for profile analysis"""
    user_id: str = Field(..., alias="userId")
    target_internship_ids: Optional[List[str]] = Field(None, alias="targetInternshipIds")
    target_roles: Optional[List[str]] = Field(None, alias="targetRoles")
    career_goals: Optional[List[str]] = Field(None, alias="careerGoals")
    include_predictions: bool = Field(True, alias="includePredictions")
    
    class Config:
        populate_by_name = True


class SkillGapAnalysisResponse(BaseModel):
    """Response model for skill gap analysis"""
    success: bool = True
    data: Optional[dict] = None
    message: Optional[str] = None


class SkillPrioritiesResponse(BaseModel):
    """Response model for skill priorities"""
    success: bool = True
    data: Optional[List[dict]] = None
    message: Optional[str] = None


class InternshipGraphResponse(BaseModel):
    """Response model for internship graph"""
    success: bool = True
    data: Optional[dict] = None
    message: Optional[str] = None


class ProjectSuggestionRequest(BaseModel):
    """Request model for project suggestions"""
    user_id: str = Field(..., alias="userId")
    target_skills: Optional[List[str]] = Field(None, alias="targetSkills")
    career_goals: Optional[List[str]] = Field(None, alias="careerGoals")
    time_available_per_week: int = Field(14, alias="timeAvailablePerWeek", ge=1, le=168)
    limit: int = Field(5, ge=1, le=20)
    
    class Config:
        populate_by_name = True


class ProjectSuggestionsResponse(BaseModel):
    """Response model for project suggestions"""
    success: bool = True
    data: Optional[List[dict]] = None
    message: Optional[str] = None


class SkillProgressPredictionResponse(BaseModel):
    """Response model for skill progress prediction"""
    success: bool = True
    data: Optional[dict] = None
    message: Optional[str] = None


class CareerReadinessPredictionResponse(BaseModel):
    """Response model for career readiness prediction"""
    success: bool = True
    data: Optional[dict] = None
    message: Optional[str] = None


@router.post("/analyze-profile", response_model=SkillGapAnalysisResponse)
async def analyze_profile(
    request: ProfileAnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze student profile and identify skill gaps
    
    This endpoint:
    1. Aggregates data from skill graph, projects, and resume
    2. Calculates current proficiency for each skill
    3. Identifies skill gaps based on target roles
    4. Prioritizes skills by impact and learning effort
    5. Generates a learning path respecting prerequisites
    
    Args:
        request: Profile analysis request with user_id, target_roles, career_goals
        
    Returns:
        SkillGapAnalysisResponse with complete analysis including:
        - Current profile snapshot
        - Skill gaps with priority scores
        - Prioritized learning path
        - Timeline estimates
    """
    try:
        user_id = current_user["user_id"]
        
        # Verify user_id matches authenticated user
        if request.user_id != user_id:
            logger.warning(f"User {user_id} attempted to analyze profile for {request.user_id}")
            raise ValidationError(
                "Cannot analyze profile for another user",
                details={"authenticated_user": user_id, "requested_user": request.user_id}
            )
        
        logger.info(f"Analyzing profile for user {user_id}, target_roles: {request.target_roles}")
        
        # Perform skill gap analysis
        analysis = await skill_gap_service.analyze_profile(request)
        
        if not analysis:
            logger.error(f"Failed to analyze profile for user {user_id}")
            raise AIServiceError("Failed to analyze profile. Please try again.")
        
        # Convert Pydantic model to dict
        analysis_dict = analysis.dict(by_alias=True)
        
        logger.info(f"Profile analysis completed for user {user_id}: {len(analysis_dict.get('skillGaps', []))} gaps identified")
        return SkillGapAnalysisResponse(
            data=analysis_dict,
            message="Profile analysis completed successfully"
        )
    
    except (ValidationError, NotFoundError, AIServiceError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error analyzing profile for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while analyzing profile"
        )


@router.get("/skill-priorities/{user_id}", response_model=SkillPrioritiesResponse)
async def get_skill_priorities(
    user_id: str,
    target_role: Optional[str] = Query(None, description="Target role for prioritization"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of skills to return"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get prioritized list of skills to learn
    
    This endpoint returns skills ordered by priority score, considering:
    - Gap size (difference between current and target proficiency)
    - Mandatory status (required for target internships)
    - Impact on eligibility (number of internships unlocked)
    - Learning effort estimates
    
    Path Parameters:
        - user_id: User identifier
        
    Query Parameters:
        - target_role: Optional target role for context-specific prioritization
        - limit: Maximum number of skills to return (default: 10, max: 50)
        
    Returns:
        SkillPrioritiesResponse with prioritized skills including:
        - Priority rank and score
        - Reasoning for prioritization
        - Internships unlocked
        - Suggested projects
    """
    try:
        authenticated_user_id = current_user["user_id"]
        
        # Verify user_id matches authenticated user
        if user_id != authenticated_user_id:
            logger.warning(f"User {authenticated_user_id} attempted to get priorities for {user_id}")
            raise ValidationError(
                "Cannot access skill priorities for another user",
                details={"authenticated_user": authenticated_user_id, "requested_user": user_id}
            )
        
        logger.info(f"Getting skill priorities for user {user_id}, target_role: {target_role}, limit: {limit}")
        
        # Build target context
        target_context = target_role if target_role else "general career development"
        
        # Get prioritized skills
        priorities = await skill_gap_service.get_skill_priorities(user_id, target_context)
        
        # Apply limit
        limited_priorities = priorities[:limit] if priorities else []
        
        logger.info(f"Retrieved {len(limited_priorities)} prioritized skills for user {user_id}")
        
        # Convert PrioritizedSkill objects to dictionaries
        priorities_dict = [skill.model_dump() if hasattr(skill, 'model_dump') else skill for skill in limited_priorities]
        
        return SkillPrioritiesResponse(
            data=priorities_dict,
            message=f"Retrieved {len(limited_priorities)} prioritized skills"
        )
    
    except (ValidationError, NotFoundError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting skill priorities for user {user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching skill priorities"
        )


@router.get("/internship-graph", response_model=InternshipGraphResponse)
async def get_internship_graph(
    skill_name: Optional[str] = Query(None, description="Filter by specific skill"),
    user_id: Optional[str] = Query(None, description="User ID for personalized graph"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get skill-internship relationship graph
    
    This endpoint provides the mapping between skills and internships:
    - Which internships require which skills
    - Proficiency requirements (min, avg, max)
    - Mandatory vs optional skills
    - Skill clusters and patterns
    - Skill dependencies and prerequisites
    
    Query Parameters:
        - skill_name: Optional filter to get internships requiring specific skill
        - user_id: Optional user ID for personalized impact analysis
        
    Returns:
        InternshipGraphResponse with:
        - Skill-internship mappings
        - Internship clusters
        - Skill dependencies
        - Total statistics
    """
    try:
        authenticated_user_id = current_user["user_id"]
        
        # If user_id provided, verify it matches authenticated user
        if user_id and user_id != authenticated_user_id:
            logger.warning(f"User {authenticated_user_id} attempted to get personalized graph for {user_id}")
            raise ValidationError(
                "Cannot access personalized graph for another user",
                details={"authenticated_user": authenticated_user_id, "requested_user": user_id}
            )
        
        logger.info(f"Getting internship graph, skill_name: {skill_name}, user_id: {user_id}")
        
        # Build the skill-internship graph
        graph = await internship_mapping_service.build_skill_internship_graph()
        
        if not graph:
            logger.error("Failed to build internship graph")
            raise AIServiceError("Failed to build internship graph. Please try again.")
        
        # Convert Pydantic model to dict
        graph_dict = graph.dict(by_alias=True)
        
        # Filter by skill_name if provided
        if skill_name:
            normalized_skill = skill_name.lower().replace(" ", "_")
            skill_mappings = graph_dict.get("skillMappings", {})
            filtered_mappings = {
                k: v for k, v in skill_mappings.items()
                if normalized_skill in k.lower() or normalized_skill in v.get("skillName", "").lower()
            }
            graph_dict["skillMappings"] = filtered_mappings
            graph_dict["totalUniqueSkills"] = len(filtered_mappings)
        
        # Add personalized impact analysis if user_id provided
        if user_id:
            # Calculate skill impact for user's current position
            # This could be enhanced to show which skills would unlock most internships
            graph_dict["personalizedForUser"] = user_id
        
        logger.info(f"Internship graph built successfully: {graph_dict.get('totalUniqueSkills', 0)} skills, {graph_dict.get('totalInternships', 0)} internships")
        return InternshipGraphResponse(
            data=graph_dict,
            message="Internship graph retrieved successfully"
        )
    
    except (ValidationError, AIServiceError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error building internship graph: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while building internship graph"
        )



@router.post("/suggest-projects", response_model=ProjectSuggestionsResponse)
async def suggest_projects(
    request: ProjectSuggestionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate personalized project suggestions
    
    This endpoint:
    1. Analyzes student's skill gaps and learning velocity
    2. Generates AI-powered project suggestions tailored to skill level
    3. Ranks projects by relevance to career goals
    4. Calculates which internships each project would unlock
    5. Provides natural language reasoning for each suggestion
    
    Args:
        request: Project suggestion request with user_id, target_skills, career_goals, time_available
        
    Returns:
        ProjectSuggestionsResponse with personalized suggestions including:
        - Project details (title, description, difficulty)
        - Relevance score (0-100)
        - Skills addressed
        - Internships unlocked
        - Estimated completion time
        - Reasoning for recommendation
    """
    try:
        authenticated_user_id = current_user["user_id"]
        
        # Verify user_id matches authenticated user
        if request.user_id != authenticated_user_id:
            logger.warning(f"User {authenticated_user_id} attempted to get suggestions for {request.user_id}")
            raise ValidationError(
                "Cannot get project suggestions for another user",
                details={"authenticated_user": authenticated_user_id, "requested_user": request.user_id}
            )
        
        logger.info(f"Generating project suggestions for user {request.user_id}, goals: {request.career_goals}")
        
        # Get skill gap analysis to build context
        from src.services.skill_gap_intelligence_service import ProfileAnalysisRequest
        
        analysis = await skill_gap_service.analyze_profile(
            ProfileAnalysisRequest(
                userId=request.user_id,
                targetRoles=request.career_goals or [],
                includePredictions=False
            )
        )
        
        if not analysis or not analysis.skill_gaps:
            logger.warning(f"No skill gaps found for user {request.user_id}")
            return ProjectSuggestionsResponse(
                data=[],
                message="No skill gaps identified. Complete a profile analysis first."
            )
        
        # Get skill graph for current proficiency levels
        skill_graph = await skill_service.get_skill_graph(request.user_id)
        
        current_proficiency_levels = {}
        if skill_graph:
            for skill in skill_graph.skills:
                current_proficiency_levels[normalize_skill_name(skill.name)] = skill.proficiency_level
        
        # Calculate learning velocity
        learning_velocity = await personalization_service.calculate_learning_velocity(request.user_id)
        
        # Get completed projects
        from src.services.project_service import project_service
        all_projects = await project_service.get_user_projects(request.user_id, status_filter=None)
        completed_projects = [p.get("projectId", "") for p in all_projects if p.get("status") == "completed"]
        
        # Filter skill gaps by target_skills if provided
        skill_gaps = analysis.skill_gaps
        if request.target_skills:
            normalized_targets = set(normalize_skill_name(s) for s in request.target_skills)
            skill_gaps = [
                g for g in skill_gaps
                if normalize_skill_name(g.skill_name) in normalized_targets
            ]
        
        if not skill_gaps:
            logger.warning(f"No matching skill gaps for target skills: {request.target_skills}")
            return ProjectSuggestionsResponse(
                data=[],
                message="No skill gaps match the specified target skills."
            )
        
        # Build personalization context
        context = PersonalizationContext(
            userId=request.user_id,
            skillGaps=[g.dict(by_alias=True) for g in skill_gaps],
            currentProficiencyLevels=current_proficiency_levels,
            careerGoals=request.career_goals or [],
            targetRoles=request.career_goals or [],
            learningVelocity=learning_velocity,
            completedProjects=completed_projects,
            timeAvailablePerWeek=request.time_available_per_week
        )
        
        # Generate suggestions
        suggestions = await personalization_service.suggest_projects(context, limit=request.limit)
        
        if not suggestions:
            logger.warning(f"Failed to generate suggestions for user {request.user_id}")
            raise AIServiceError("Failed to generate project suggestions. Please try again.")
        
        # Convert to dict
        suggestions_dict = [s.dict(by_alias=True) for s in suggestions]
        
        logger.info(f"Generated {len(suggestions_dict)} project suggestions for user {request.user_id}")
        return ProjectSuggestionsResponse(
            data=suggestions_dict,
            message=f"Generated {len(suggestions_dict)} personalized project suggestions"
        )
    
    except (ValidationError, NotFoundError, AIServiceError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating project suggestions for user {current_user.get('user_id')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating project suggestions"
        )


@router.get("/predict/skill-progress/{user_id}/{skill_name}", response_model=SkillProgressPredictionResponse)
async def predict_skill_progress(
    user_id: str,
    skill_name: str,
    target_proficiency: int = Query(80, ge=0, le=100, description="Target proficiency level (0-100)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Predict skill progress timeline
    
    This endpoint:
    1. Analyzes student's current proficiency in the skill
    2. Calculates learning velocity from historical data
    3. Estimates time to reach target proficiency
    4. Generates learning trajectory with milestones
    5. Recommends projects to accelerate learning
    6. Identifies blockers (unmet prerequisites)
    
    Path Parameters:
        - user_id: User identifier
        - skill_name: Name of the skill to predict progress for
        
    Query Parameters:
        - target_proficiency: Target proficiency level (default: 80, range: 0-100)
        
    Returns:
        SkillProgressPredictionResponse with:
        - Current and target proficiency
        - Estimated days to reach target
        - Confidence level (0-100)
        - Learning trajectory with milestones
        - Recommended projects
        - Blockers (prerequisites not met)
    """
    try:
        authenticated_user_id = current_user["user_id"]
        
        # Verify user_id matches authenticated user
        if user_id != authenticated_user_id:
            logger.warning(f"User {authenticated_user_id} attempted to predict progress for {user_id}")
            raise ValidationError(
                "Cannot predict skill progress for another user",
                details={"authenticated_user": authenticated_user_id, "requested_user": user_id}
            )
        
        # Validate target_proficiency
        if target_proficiency < 0 or target_proficiency > 100:
            raise ValidationError(
                "Target proficiency must be between 0 and 100",
                details={"target_proficiency": target_proficiency}
            )
        
        logger.info(f"Predicting skill progress for user {user_id}, skill {skill_name}, target {target_proficiency}%")
        
        # Generate prediction
        prediction = await prediction_service.predict_skill_progress(
            user_id,
            skill_name,
            target_proficiency
        )
        
        if not prediction:
            logger.error(f"Failed to generate prediction for user {user_id}, skill {skill_name}")
            raise AIServiceError("Failed to generate skill progress prediction. Please try again.")
        
        # Convert to dict
        prediction_dict = prediction.dict(by_alias=True)
        
        logger.info(f"Skill progress prediction complete: {prediction.estimated_days_to_target} days to {target_proficiency}%")
        return SkillProgressPredictionResponse(
            data=prediction_dict,
            message=f"Estimated {prediction.estimated_days_to_target} days to reach {target_proficiency}% proficiency"
        )
    
    except (ValidationError, NotFoundError, AIServiceError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error predicting skill progress for user {user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while predicting skill progress"
        )


@router.get("/predict/career-readiness/{user_id}/{target_role}", response_model=CareerReadinessPredictionResponse)
async def predict_career_readiness(
    user_id: str,
    target_role: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Predict career readiness for target role
    
    This endpoint:
    1. Identifies internships matching the target role
    2. Analyzes skill gaps for those internships
    3. Calculates current readiness score (0-100)
    4. Estimates time to reach 80% readiness
    5. Provides missing skills with priorities
    6. Generates recommended learning path
    7. Creates milestone predictions (25%, 50%, 75%, 100%)
    
    Path Parameters:
        - user_id: User identifier
        - target_role: Target career role (e.g., "Software Engineer", "Data Scientist")
        
    Returns:
        CareerReadinessPredictionResponse with:
        - Current and target readiness scores
        - Estimated months to ready
        - Confidence level (0-100)
        - Missing skills with gap details
        - Recommended learning path
        - Milestone predictions with dates
    """
    try:
        authenticated_user_id = current_user["user_id"]
        
        # Verify user_id matches authenticated user
        if user_id != authenticated_user_id:
            logger.warning(f"User {authenticated_user_id} attempted to predict readiness for {user_id}")
            raise ValidationError(
                "Cannot predict career readiness for another user",
                details={"authenticated_user": authenticated_user_id, "requested_user": user_id}
            )
        
        # Validate target_role
        if not target_role or len(target_role.strip()) == 0:
            raise ValidationError(
                "Target role cannot be empty",
                details={"target_role": target_role}
            )
        
        logger.info(f"Predicting career readiness for user {user_id}, role {target_role}")
        
        # Generate prediction
        prediction = await prediction_service.predict_career_readiness(
            user_id,
            target_role
        )
        
        if not prediction:
            logger.error(f"Failed to generate readiness prediction for user {user_id}, role {target_role}")
            raise AIServiceError("Failed to generate career readiness prediction. Please try again.")
        
        # Convert to dict
        prediction_dict = prediction.dict(by_alias=True)
        
        logger.info(f"Career readiness prediction complete: {prediction.estimated_months_to_ready} months to ready")
        return CareerReadinessPredictionResponse(
            data=prediction_dict,
            message=f"Estimated {prediction.estimated_months_to_ready} months to reach readiness for {target_role}"
        )
    
    except (ValidationError, NotFoundError, AIServiceError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error predicting career readiness for user {user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while predicting career readiness"
        )


# Phase 3: Career Planning and Explanation Endpoints

class CareerRoadmapRequest(BaseModel):
    """Request for career roadmap generation"""
    user_id: str = Field(alias="userId")
    target_role: str = Field(alias="targetRole")
    timeline_months: int = Field(6, alias="timelineMonths", ge=1, le=24)
    
    class Config:
        populate_by_name = True


class RoadmapProgressUpdate(BaseModel):
    """Update for roadmap progress"""
    milestone_id: str = Field(alias="milestoneId")
    status: str  # "not_started", "in_progress", "completed"
    notes: Optional[str] = None
    
    class Config:
        populate_by_name = True


class ExplanationRequest(BaseModel):
    """Request for explanation generation"""
    user_id: str = Field(alias="userId")
    explanation_type: str = Field(alias="explanationType")
    context: Dict[str, Any]
    
    class Config:
        populate_by_name = True


@router.post("/career-roadmap", response_model=Dict[str, Any])
async def generate_career_roadmap(
    request: CareerRoadmapRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate personalized career roadmap
    
    Creates 3-5 progressive milestones from current position to target role
    with project suggestions and internship targets for each milestone.
    
    **Requirements**: User must have profile and skills
    
    **Returns**: Complete career roadmap with milestones, timeline, and progress tracking
    """
    try:
        logger.info(f"Generating career roadmap for user: {request.user_id}, role: {request.target_role}")
        
        # Verify user owns the profile
        if current_user["userId"] != request.user_id:
            raise HTTPException(
                status_code=403,
                detail="Cannot generate roadmap for another user"
            )
        
        # Import career path service
        from src.services.career_path_service import career_path_service
        
        # Generate roadmap
        roadmap = await career_path_service.generate_roadmap(
            user_id=request.user_id,
            target_role=request.target_role,
            timeline_months=request.timeline_months
        )
        
        logger.info(f"Career roadmap generated: {roadmap.roadmap_id}")
        
        return {
            "success": True,
            "roadmap": roadmap.dict(by_alias=True),
            "message": f"Career roadmap generated with {len(roadmap.milestones)} milestones"
        }
    
    except ValueError as e:
        logger.error(f"Validation error generating roadmap: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generating career roadmap: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate career roadmap"
        )


@router.put("/career-roadmap/{roadmap_id}/progress", response_model=Dict[str, Any])
async def update_roadmap_progress(
    roadmap_id: str,
    update: RoadmapProgressUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update progress on a roadmap milestone
    
    Tracks completion status and recalculates overall roadmap progress.
    
    **Status values**: "not_started", "in_progress", "completed"
    
    **Returns**: Updated roadmap with new progress percentage
    """
    try:
        logger.info(f"Updating roadmap {roadmap_id}, milestone {update.milestone_id}")
        
        # Import career path service
        from src.services.career_path_service import career_path_service
        
        # Update progress
        updated_roadmap = await career_path_service.update_roadmap_progress(
            roadmap_id=roadmap_id,
            milestone_id=update.milestone_id,
            status=update.status,
            notes=update.notes
        )
        
        # Verify user owns the roadmap
        if updated_roadmap.user_id != current_user["userId"]:
            raise HTTPException(
                status_code=403,
                detail="Cannot update another user's roadmap"
            )
        
        logger.info(f"Roadmap progress updated: {updated_roadmap.dict(by_alias=True).get('progressPercentage', 0)}%")
        
        return {
            "success": True,
            "roadmap": updated_roadmap.dict(by_alias=True),
            "message": f"Milestone status updated to {update.status}"
        }
    
    except ValueError as e:
        logger.error(f"Validation error updating roadmap: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error updating roadmap progress: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to update roadmap progress"
        )


@router.get("/next-steps/{user_id}/{roadmap_id}", response_model=Dict[str, Any])
async def get_next_steps(
    user_id: str,
    roadmap_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get suggested next steps for career roadmap
    
    Analyzes current progress and suggests prioritized actions including:
    - Skills to learn
    - Projects to complete
    - Internships to apply to
    - AI-powered recommendations
    
    **Returns**: Prioritized list of next actionable steps
    """
    try:
        logger.info(f"Getting next steps for user: {user_id}, roadmap: {roadmap_id}")
        
        # Verify user owns the roadmap
        if current_user["userId"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="Cannot access another user's roadmap"
            )
        
        # Import career path service
        from src.services.career_path_service import career_path_service
        
        # Get next steps
        next_steps = await career_path_service.suggest_next_steps(
            user_id=user_id,
            roadmap_id=roadmap_id
        )
        
        logger.info(f"Next steps generated: {len(next_steps.get('nextSteps', []))} steps")
        
        return {
            "success": True,
            "data": next_steps,
            "message": "Next steps generated successfully"
        }
    
    except ValueError as e:
        logger.error(f"Validation error getting next steps: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error getting next steps: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get next steps"
        )


@router.post("/explain", response_model=Dict[str, Any])
async def generate_explanation(
    request: ExplanationRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate explanation for a recommendation
    
    Provides clear, factor-based explanations for:
    - Internship matches
    - Project suggestions
    - Skill priorities
    - Career milestones
    
    **Explanation Types**:
    - "internship_match": Explain why an internship is a good/bad match
    - "project_suggestion": Explain why a project is recommended
    - "skill_priority": Explain why a skill is high/low priority
    - "career_step": Explain why a milestone is important
    
    **Returns**: Detailed explanation with factors, confidence, and recommendations
    """
    try:
        logger.info(f"Generating explanation type: {request.explanation_type} for user: {request.user_id}")
        
        # Verify user owns the data
        if current_user["userId"] != request.user_id:
            raise HTTPException(
                status_code=403,
                detail="Cannot generate explanation for another user"
            )
        
        # Import explanation service
        from src.services.explanation_service import explanation_service
        
        # Generate explanation based on type
        if request.explanation_type == "internship_match":
            explanation = await explanation_service.explain_internship_match(
                user_id=request.user_id,
                internship_id=request.context["internshipId"],
                match_score=request.context["matchScore"],
                matched_skills=request.context.get("matchedSkills", []),
                missing_skills=request.context.get("missingSkills", [])
            )
        
        elif request.explanation_type == "project_suggestion":
            explanation = await explanation_service.explain_project_suggestion(
                user_id=request.user_id,
                project_id=request.context["projectId"],
                relevance_score=request.context["relevanceScore"],
                target_skills=request.context.get("targetSkills", []),
                internships_unlocked=request.context.get("internshipsUnlocked", 0)
            )
        
        elif request.explanation_type == "skill_priority":
            explanation = await explanation_service.explain_skill_priority(
                user_id=request.user_id,
                skill_name=request.context["skillName"],
                priority_score=request.context["priorityScore"],
                internships_impacted=request.context.get("internshipsImpacted", 0),
                gap_size=request.context.get("gapSize", 0)
            )
        
        elif request.explanation_type == "career_step":
            explanation = await explanation_service.explain_career_step(
                user_id=request.user_id,
                milestone_title=request.context["milestoneTitle"],
                milestone_description=request.context.get("milestoneDescription", ""),
                skills_to_acquire=request.context.get("skillsToAcquire", []),
                estimated_weeks=request.context.get("estimatedWeeks", 4)
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown explanation type: {request.explanation_type}"
            )
        
        logger.info(f"Explanation generated: {explanation.explanation_id}")
        
        return {
            "success": True,
            "explanation": explanation.dict(by_alias=True),
            "message": "Explanation generated successfully"
        }
    
    except ValueError as e:
        logger.error(f"Validation error generating explanation: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate explanation"
        )
