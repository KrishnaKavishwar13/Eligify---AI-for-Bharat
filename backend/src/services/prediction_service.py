"""Prediction Service - Predicts skill progress and career readiness"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

from src.services.skill_service import skill_service
from src.services.project_service import project_service
from src.services.personalization_service import personalization_service
from src.services.skill_gap_intelligence_service import (
    skill_gap_intelligence_service,
    ProfileAnalysisRequest
)
from src.utils.validation import normalize_skill_name
from src.utils.mock_store import mock_store

logger = logging.getLogger(__name__)


# Data Models
class SkillProgressPrediction(BaseModel):
    """Prediction of skill progress over time"""
    skill_name: str = Field(alias="skillName")
    current_proficiency: int = Field(alias="currentProficiency", ge=0, le=100)
    target_proficiency: int = Field(alias="targetProficiency", ge=0, le=100)
    estimated_days_to_target: int = Field(alias="estimatedDaysToTarget")
    confidence_level: float = Field(alias="confidenceLevel", ge=0, le=100)
    learning_trajectory: List[Dict[str, Any]] = Field(alias="learningTrajectory")
    recommended_projects: List[str] = Field(default_factory=list, alias="recommendedProjects")
    blockers: List[str] = Field(default_factory=list)

    class Config:
        populate_by_name = True


class CareerReadinessPrediction(BaseModel):
    """Prediction of career readiness"""
    target_role: str = Field(alias="targetRole")
    current_readiness_score: float = Field(alias="currentReadinessScore", ge=0, le=100)
    target_readiness_score: float = Field(alias="targetReadinessScore", ge=0, le=100)
    estimated_months_to_ready: float = Field(alias="estimatedMonthsToReady")
    confidence_level: float = Field(alias="confidenceLevel", ge=0, le=100)
    missing_skills: List[Dict[str, Any]] = Field(alias="missingSkills")
    recommended_path: List[str] = Field(alias="recommendedPath")
    milestone_predictions: List[Dict[str, Any]] = Field(alias="milestonePredictions")

    class Config:
        populate_by_name = True


class PredictionService:
    """Service for predicting skill progress and career readiness"""
    
    async def predict_skill_progress(
        self,
        user_id: str,
        skill_name: str,
        target_proficiency: int
    ) -> SkillProgressPrediction:
        """
        Predict skill progress timeline
        
        Estimates when a student will reach target proficiency based on
        current proficiency and learning velocity
        """
        logger.info(f"Predicting skill progress for user {user_id}, skill {skill_name}")
        
        # Get current proficiency from skill service
        skill_graph = await skill_service.get_skill_graph(user_id)
        
        current_proficiency = 0
        if skill_graph:
            skill_key = normalize_skill_name(skill_name)
            for skill in skill_graph.skills:
                if normalize_skill_name(skill.name) == skill_key:
                    current_proficiency = skill.proficiency_level
                    break
        
        # Ensure target is greater than current
        if target_proficiency <= current_proficiency:
            target_proficiency = min(current_proficiency + 10, 100)
        
        # Get learning velocity from personalization service
        learning_velocity = await personalization_service.calculate_learning_velocity(user_id)
        
        # Calculate gap and estimate days
        gap_size = target_proficiency - current_proficiency
        
        # Base calculation: 2 hours per proficiency point
        base_hours_per_point = 2.0
        total_hours_needed = gap_size * base_hours_per_point
        
        # Adjust based on learning velocity
        # Average completion time tells us how fast they work
        avg_days = learning_velocity.average_project_completion_time
        platform_avg_days = 14.0
        
        # Calculate velocity factor (1.0 = average, >1.0 = slower, <1.0 = faster)
        velocity_factor = avg_days / platform_avg_days
        
        # Adjust hours based on velocity
        adjusted_hours = total_hours_needed * velocity_factor
        
        # Assume 2 hours per day of focused learning
        hours_per_day = 2.0
        estimated_days = int(adjusted_hours / hours_per_day)
        
        # Generate learning trajectory (milestones every 10% proficiency)
        learning_trajectory = self.calculate_learning_trajectory(
            current_proficiency,
            target_proficiency,
            learning_velocity.skill_acquisition_rate
        )
        
        # Calculate confidence based on historical data
        confidence = self.calculate_prediction_confidence(
            learning_velocity.projects_completed_last_30_days,
            estimated_days,
            learning_velocity.consistency_score
        )
        
        # Get recommended projects for this skill
        recommended_projects = []
        try:
            # Get skill gaps to build context
            analysis = await skill_gap_intelligence_service.analyze_profile(
                ProfileAnalysisRequest(
                    userId=user_id,
                    targetInternshipIds=[],
                    includePredictions=False
                )
            )
            
            # Find this skill in gaps
            skill_gaps = [g for g in analysis.skill_gaps if normalize_skill_name(g.skill_name) == normalize_skill_name(skill_name)]
            
            if skill_gaps:
                # Use personalization service to suggest projects
                from src.services.personalization_service import PersonalizationContext
                
                context = PersonalizationContext(
                    userId=user_id,
                    skillGaps=[g.dict(by_alias=True) for g in skill_gaps],
                    currentProficiencyLevels={normalize_skill_name(s.name): s.proficiency_level for s in skill_graph.skills} if skill_graph else {},
                    careerGoals=[],
                    targetRoles=[],
                    learningVelocity=learning_velocity,
                    completedProjects=[],
                    timeAvailablePerWeek=14  # 2 hours/day * 7 days
                )
                
                suggestions = await personalization_service.suggest_projects(context, limit=3)
                recommended_projects = [s.project_id for s in suggestions]
        except Exception as e:
            logger.warning(f"Could not get recommended projects: {e}")
        
        # Identify blockers (prerequisites not met)
        blockers = []
        if skill_graph:
            for skill in skill_graph.skills:
                if normalize_skill_name(skill.name) == normalize_skill_name(skill_name):
                    # Check if prerequisites are met
                    for prereq in skill.prerequisites:
                        prereq_skill = next(
                            (s for s in skill_graph.skills if normalize_skill_name(s.name) == normalize_skill_name(prereq)),
                            None
                        )
                        if not prereq_skill or prereq_skill.proficiency_level < 50:
                            blockers.append(f"Prerequisite skill '{prereq}' not sufficiently developed")
                    break
        
        prediction = SkillProgressPrediction(
            skillName=skill_name,
            currentProficiency=current_proficiency,
            targetProficiency=target_proficiency,
            estimatedDaysToTarget=estimated_days,
            confidenceLevel=confidence,
            learningTrajectory=learning_trajectory,
            recommendedProjects=recommended_projects,
            blockers=blockers
        )
        
        # Cache prediction (24 hours)
        cache_key = f"{user_id}_{normalize_skill_name(skill_name)}"
        cache_data = {
            "prediction": prediction.dict(by_alias=True),
            "createdAt": datetime.utcnow().isoformat(),
            "expiresAt": (datetime.utcnow() + timedelta(hours=24)).isoformat()
        }
        mock_store.save_prediction(cache_key, cache_data)
        
        logger.info(f"Skill progress prediction complete: {estimated_days} days to reach {target_proficiency}%")
        return prediction
    
    async def predict_career_readiness(
        self,
        user_id: str,
        target_role: str
    ) -> CareerReadinessPrediction:
        """
        Predict career readiness for target role
        
        Estimates when student will be ready for target role based on
        skill gaps and learning velocity
        """
        logger.info(f"Predicting career readiness for user {user_id}, role {target_role}")
        
        # Get skill graph
        skill_graph = await skill_service.get_skill_graph(user_id)
        
        # Get all internships and filter by role
        all_internships = mock_store.get_all_internships()
        role_internships = [
            i for i in all_internships
            if target_role.lower() in i.get("title", "").lower() or
               target_role.lower() in i.get("description", "").lower()
        ]
        
        if not role_internships:
            # No matching internships, use generic calculation
            logger.warning(f"No internships found for role: {target_role}")
            return CareerReadinessPrediction(
                targetRole=target_role,
                currentReadinessScore=0.0,
                targetReadinessScore=80.0,
                estimatedMonthsToReady=6.0,
                confidenceLevel=30.0,
                missingSkills=[],
                recommendedPath=[],
                milestonePredictions=[]
            )
        
        # Analyze skill gaps for these internships
        internship_ids = [i["internshipId"] for i in role_internships[:5]]  # Top 5
        
        analysis = await skill_gap_intelligence_service.analyze_profile(
            ProfileAnalysisRequest(
                userId=user_id,
                targetInternshipIds=internship_ids,
                targetRoles=[target_role],
                includePredictions=True
            )
        )
        
        # Calculate current readiness score
        # Based on: verified skills / total required skills * 100
        if analysis.skill_gaps:
            total_required_proficiency = sum(g.target_proficiency for g in analysis.skill_gaps)
            current_total_proficiency = sum(g.current_proficiency for g in analysis.skill_gaps)
            
            if total_required_proficiency > 0:
                current_readiness = (current_total_proficiency / total_required_proficiency) * 100
            else:
                current_readiness = 100.0
        else:
            current_readiness = 100.0
        
        # Target readiness score (80% is considered "ready")
        target_readiness = 80.0
        
        # Get learning velocity
        learning_velocity = await personalization_service.calculate_learning_velocity(user_id)
        
        # Estimate time to close all gaps
        total_hours = sum(g.estimated_learning_hours for g in analysis.skill_gaps)
        
        # Adjust based on learning velocity
        avg_days = learning_velocity.average_project_completion_time
        platform_avg_days = 14.0
        velocity_factor = avg_days / platform_avg_days
        
        adjusted_hours = total_hours * velocity_factor
        
        # Assume 10 hours per week of learning
        hours_per_week = 10.0
        estimated_weeks = adjusted_hours / hours_per_week
        estimated_months = estimated_weeks / 4.0
        
        # Calculate confidence
        confidence = self.calculate_prediction_confidence(
            learning_velocity.projects_completed_last_30_days,
            int(estimated_weeks * 7),  # Convert to days
            learning_velocity.consistency_score
        )
        
        # Build missing skills list
        missing_skills = [
            {
                "skillName": g.skill_name,
                "currentProficiency": g.current_proficiency,
                "targetProficiency": g.target_proficiency,
                "gapSize": g.gap_size,
                "priorityScore": g.priority_score
            }
            for g in analysis.skill_gaps
        ]
        
        # Build recommended path (learning path from analysis)
        recommended_path = analysis.learning_path
        
        # Generate milestone predictions (every 25% of progress)
        milestone_predictions = []
        total_skills = len(analysis.skill_gaps)
        
        if total_skills > 0:
            for milestone_pct in [25, 50, 75, 100]:
                skills_at_milestone = int(total_skills * milestone_pct / 100)
                hours_at_milestone = int(adjusted_hours * milestone_pct / 100)
                weeks_at_milestone = hours_at_milestone / hours_per_week
                
                milestone_date = datetime.utcnow() + timedelta(weeks=weeks_at_milestone)
                
                milestone_predictions.append({
                    "milestone": f"{milestone_pct}% Complete",
                    "skillsCompleted": skills_at_milestone,
                    "estimatedDate": milestone_date.isoformat(),
                    "estimatedWeeks": round(weeks_at_milestone, 1),
                    "readinessScore": current_readiness + (target_readiness - current_readiness) * milestone_pct / 100
                })
        
        prediction = CareerReadinessPrediction(
            targetRole=target_role,
            currentReadinessScore=round(current_readiness, 2),
            targetReadinessScore=target_readiness,
            estimatedMonthsToReady=round(estimated_months, 1),
            confidenceLevel=confidence,
            missingSkills=missing_skills,
            recommendedPath=recommended_path,
            milestonePredictions=milestone_predictions
        )
        
        # Cache prediction (24 hours)
        cache_key = f"{user_id}_{normalize_skill_name(target_role)}_readiness"
        cache_data = {
            "prediction": prediction.dict(by_alias=True),
            "createdAt": datetime.utcnow().isoformat(),
            "expiresAt": (datetime.utcnow() + timedelta(hours=24)).isoformat()
        }
        mock_store.save_prediction(cache_key, cache_data)
        
        logger.info(f"Career readiness prediction complete: {estimated_months:.1f} months to ready")
        return prediction
    
    async def estimate_project_completion(
        self,
        user_id: str,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Estimate project completion timeline
        
        Returns estimate with confidence bounds based on user's learning velocity
        """
        logger.info(f"Estimating project completion for user {user_id}, project {project_id}")
        
        # Get project details
        project = mock_store.get_project(project_id)
        
        if not project:
            logger.warning(f"Project not found: {project_id}")
            return {
                "projectId": project_id,
                "estimatedDays": 14,
                "confidenceLower": 10,
                "confidenceUpper": 20,
                "confidence": 30.0
            }
        
        # Get learning velocity
        learning_velocity = await personalization_service.calculate_learning_velocity(user_id)
        
        # Base estimate from project
        base_hours = project.get("estimatedHours", 40)
        
        # Adjust based on learning velocity
        avg_days = learning_velocity.average_project_completion_time
        platform_avg_days = 14.0
        velocity_factor = avg_days / platform_avg_days
        
        adjusted_hours = base_hours * velocity_factor
        
        # Assume 2 hours per day
        hours_per_day = 2.0
        estimated_days = int(adjusted_hours / hours_per_day)
        
        # Calculate confidence bounds (±20%)
        confidence_lower = int(estimated_days * 0.8)
        confidence_upper = int(estimated_days * 1.2)
        
        # Calculate confidence based on data quality
        confidence = self.calculate_prediction_confidence(
            learning_velocity.projects_completed_last_30_days,
            estimated_days,
            learning_velocity.consistency_score
        )
        
        return {
            "projectId": project_id,
            "estimatedDays": estimated_days,
            "confidenceLower": confidence_lower,
            "confidenceUpper": confidence_upper,
            "confidence": confidence,
            "estimatedCompletionDate": (datetime.utcnow() + timedelta(days=estimated_days)).isoformat()
        }
    
    def calculate_learning_trajectory(
        self,
        current_proficiency: int,
        target_proficiency: int,
        learning_velocity: float
    ) -> List[Dict[str, Any]]:
        """
        Calculate learning trajectory with milestones
        
        Models learning curve (logarithmic growth) and generates proficiency
        milestones every 10% with estimated time for each
        """
        trajectory = []
        
        # Generate milestones every 10 proficiency points
        milestone_interval = 10
        
        current = current_proficiency
        days_accumulated = 0
        
        while current < target_proficiency:
            next_milestone = min(current + milestone_interval, target_proficiency)
            gap = next_milestone - current
            
            # Base hours per point (2 hours)
            base_hours = gap * 2.0
            
            # Apply logarithmic learning curve (later milestones take longer)
            # As proficiency increases, each point becomes harder
            difficulty_factor = 1.0 + (next_milestone / 100) * 0.5
            adjusted_hours = base_hours * difficulty_factor
            
            # Adjust for learning velocity
            # Higher velocity (more skills/month) = faster learning
            velocity_adjustment = max(0.5, 2.0 / max(learning_velocity, 0.5))
            final_hours = adjusted_hours * velocity_adjustment
            
            # Convert to days (2 hours per day)
            days_for_milestone = int(final_hours / 2.0)
            days_accumulated += days_for_milestone
            
            milestone_date = datetime.utcnow() + timedelta(days=days_accumulated)
            
            trajectory.append({
                "proficiency": next_milestone,
                "days": days_accumulated,
                "date": milestone_date.isoformat(),
                "hoursRequired": int(final_hours)
            })
            
            current = next_milestone
        
        return trajectory
    
    def calculate_prediction_confidence(
        self,
        projects_completed_last_30_days: int,
        prediction_distance_days: int,
        consistency_score: float
    ) -> float:
        """
        Calculate confidence score for predictions
        
        Confidence decreases with:
        - Less historical data (fewer completed projects)
        - Longer prediction distance (further into future)
        - Lower consistency score
        """
        # Base confidence
        confidence = 70.0
        
        # Increase with more recent activity (up to +20)
        activity_bonus = min(projects_completed_last_30_days * 5, 20)
        confidence += activity_bonus
        
        # Decrease with prediction distance (up to -30)
        # Predictions beyond 12 weeks (84 days) have reduced confidence
        if prediction_distance_days > 84:
            distance_penalty = min((prediction_distance_days - 84) / 7, 30)
            confidence -= distance_penalty
        
        # Adjust based on consistency score
        # High consistency = more reliable predictions
        consistency_adjustment = (consistency_score - 50) / 5
        confidence += consistency_adjustment
        
        # Ensure bounds
        confidence = max(min(confidence, 100.0), 0.0)
        
        return round(confidence, 2)


# Add storage methods to mock_store
def save_prediction(cache_key: str, prediction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Save prediction to cache"""
    if not hasattr(mock_store, '_predictions'):
        mock_store._predictions = {}
    mock_store._predictions[cache_key] = prediction_data
    return prediction_data


def get_prediction(cache_key: str) -> Optional[Dict[str, Any]]:
    """Get cached prediction"""
    if not hasattr(mock_store, '_predictions'):
        return None
    
    cached = mock_store._predictions.get(cache_key)
    
    if cached:
        # Check expiration
        expires_at = datetime.fromisoformat(cached["expiresAt"])
        if datetime.utcnow() < expires_at:
            return cached
        else:
            # Expired, remove from cache
            del mock_store._predictions[cache_key]
    
    return None


# Monkey-patch mock_store with prediction methods
mock_store.save_prediction = save_prediction
mock_store.get_prediction = get_prediction


# Export singleton
prediction_service = PredictionService()
