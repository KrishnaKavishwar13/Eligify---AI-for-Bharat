"""Skill Gap Intelligence Service - Analyzes student profiles and identifies skill gaps"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

from src.services.skill_service import skill_service
from src.services.project_service import project_service
from src.utils.validation import normalize_skill_name
from src.utils.mock_store import mock_store

logger = logging.getLogger(__name__)


# Data Models
class CurrentProfile(BaseModel):
    """Student's current profile snapshot"""
    total_skills: int = Field(alias="totalSkills")
    verified_skills: int = Field(alias="verifiedSkills")
    in_progress_skills: int = Field(alias="inProgressSkills")
    completed_projects: int = Field(alias="completedProjects")
    average_proficiency: float = Field(alias="averageProficiency")
    skill_categories: Dict[str, int] = Field(alias="skillCategories")

    class Config:
        populate_by_name = True


class SkillGap(BaseModel):
    """Individual skill gap"""
    skill_name: str = Field(alias="skillName")
    normalized_name: str = Field(alias="normalizedName")
    category: str
    current_proficiency: int = Field(alias="currentProficiency", ge=0, le=100)
    target_proficiency: int = Field(alias="targetProficiency", ge=0, le=100)
    gap_size: int = Field(alias="gapSize")
    priority_score: float = Field(alias="priorityScore", ge=0, le=100)
    impact_on_eligibility: int = Field(alias="impactOnEligibility")
    estimated_learning_hours: int = Field(alias="estimatedLearningHours")
    prerequisites: List[str] = []
    related_skills: List[str] = Field(default_factory=list, alias="relatedSkills")

    class Config:
        populate_by_name = True


class PrioritizedSkill(BaseModel):
    """Skill with priority ranking"""
    skill_name: str = Field(alias="skillName")
    priority_rank: int = Field(alias="priorityRank")
    priority_score: float = Field(alias="priorityScore")
    reasoning: str
    internships_unlocked: int = Field(alias="internshipsUnlocked")
    suggested_projects: List[str] = Field(default_factory=list, alias="suggestedProjects")

    class Config:
        populate_by_name = True


class SkillGapAnalysis(BaseModel):
    """Complete skill gap analysis"""
    user_id: str = Field(alias="userId")
    analysis_id: str = Field(alias="analysisId")
    current_profile: CurrentProfile = Field(alias="currentProfile")
    skill_gaps: List[SkillGap] = Field(alias="skillGaps")
    prioritized_skills: List[PrioritizedSkill] = Field(alias="prioritizedSkills")
    learning_path: List[str] = Field(alias="learningPath")
    estimated_timeline: str = Field(alias="estimatedTimeline")
    confidence_score: float = Field(alias="confidenceScore", ge=0, le=100)
    target_internships: Optional[List[str]] = Field(None, alias="targetInternships")
    target_roles: Optional[List[str]] = Field(None, alias="targetRoles")
    created_at: str = Field(alias="createdAt")
    expires_at: str = Field(alias="expiresAt")

    class Config:
        populate_by_name = True


class ProfileAnalysisRequest(BaseModel):
    """Request for comprehensive profile analysis"""
    user_id: str = Field(alias="userId")
    target_internship_ids: Optional[List[str]] = Field(None, alias="targetInternshipIds")
    target_roles: Optional[List[str]] = Field(None, alias="targetRoles")
    include_predictions: bool = Field(True, alias="includePredictions")

    class Config:
        populate_by_name = True


class SkillGapIntelligenceService:
    """Service for analyzing student profiles and identifying skill gaps"""
    
    @staticmethod
    def calculate_priority_score(
        gap_size: int,
        mandatory_count: int,
        total_count: int,
        weight_sum: float
    ) -> float:
        """
        Calculate priority score for skill gap
        
        Priority = (0.4 * gap_urgency) + (0.3 * mandatory_factor) + (0.3 * impact_factor)
        
        Returns score between 0 and 100
        """
        # Gap urgency: larger gaps are more urgent (0-100)
        gap_urgency = min(gap_size * 1.2, 100)
        
        # Mandatory factor: mandatory skills get higher priority (0-100)
        mandatory_ratio = mandatory_count / total_count if total_count > 0 else 0
        mandatory_factor = mandatory_ratio * 100
        
        # Impact factor: skills required by more internships (0-100)
        # Normalize by assuming max 10 internships require same skill
        impact_factor = min((total_count / 10) * 100, 100)
        
        # Weighted combination
        priority_score = (0.4 * gap_urgency) + (0.3 * mandatory_factor) + (0.3 * impact_factor)
        
        return round(priority_score, 2)
    
    @staticmethod
    def topological_sort_skills(skill_gaps: List[SkillGap]) -> List[str]:
        """
        Sort skills by dependencies using topological sort (Kahn's algorithm)
        
        Returns ordered list where prerequisites appear before dependent skills
        """
        if not skill_gaps:
            return []
        
        # Build adjacency list and in-degree map
        graph = {}
        in_degree = {}
        
        for gap in skill_gaps:
            skill = gap.skill_name
            graph[skill] = gap.prerequisites
            in_degree[skill] = 0
        
        # Calculate in-degrees
        for skill in graph:
            for prereq in graph[skill]:
                if prereq in in_degree:
                    in_degree[skill] += 1
        
        # Kahn's algorithm
        queue = [skill for skill in in_degree if in_degree[skill] == 0]
        result = []
        
        while queue:
            # Sort by priority if available
            queue.sort(key=lambda s: next(
                (gap.priority_score for gap in skill_gaps if gap.skill_name == s), 0
            ), reverse=True)
            
            skill = queue.pop(0)
            result.append(skill)
            
            # Update in-degrees for dependent skills
            for dependent in graph:
                if skill in graph[dependent]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)
        
        # If not all skills processed, there's a cycle - add remaining by priority
        if len(result) < len(skill_gaps):
            remaining = [gap.skill_name for gap in skill_gaps if gap.skill_name not in result]
            logger.warning(f"Circular dependency detected in skills: {remaining}")
            result.extend(remaining)
        
        return result
    
    @staticmethod
    def estimate_learning_hours(gap_size: int, category: str, learning_velocity: float = 1.0) -> int:
        """Estimate learning hours based on gap size and category"""
        # Base hours per proficiency point
        base_hours_map = {
            "programming_language": 2.0,
            "framework": 1.5,
            "tool": 1.0,
            "soft_skill": 0.5,
            "domain_knowledge": 1.2
        }
        
        base_hours = base_hours_map.get(category, 1.0)
        estimated = gap_size * base_hours / learning_velocity
        
        return max(int(estimated), 1)
    
    @staticmethod
    def calculate_average_proficiency(skills: List[Dict[str, Any]]) -> float:
        """Calculate average proficiency across all skills"""
        if not skills:
            return 0.0
        
        total = sum(skill.get("proficiencyLevel", 0) for skill in skills)
        return round(total / len(skills), 2)
    
    @staticmethod
    def categorize_skills(skills: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count skills by category"""
        categories = {}
        for skill in skills:
            category = skill.get("category", "tool")
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    async def analyze_profile(
        self,
        request: ProfileAnalysisRequest
    ) -> SkillGapAnalysis:
        """
        Analyze complete student profile and identify skill gaps
        
        Returns comprehensive analysis with prioritized skills and learning path
        """
        user_id = request.user_id
        logger.info(f"Starting profile analysis for user: {user_id}")
        
        # Step 1: Gather current profile data
        skill_graph = await skill_service.get_skill_graph(user_id)
        
        if not skill_graph or not skill_graph.skills:
            # No profile data - return empty analysis
            logger.warning(f"No profile data for user: {user_id}")
            return SkillGapAnalysis(
                userId=user_id,
                analysisId=str(uuid4()),
                currentProfile=CurrentProfile(
                    totalSkills=0,
                    verifiedSkills=0,
                    inProgressSkills=0,
                    completedProjects=0,
                    averageProficiency=0.0,
                    skillCategories={}
                ),
                skillGaps=[],
                prioritizedSkills=[],
                learningPath=[],
                estimatedTimeline="Unknown - please add skills first",
                confidenceScore=0.0,
                targetInternships=request.target_internship_ids,
                targetRoles=request.target_roles,
                createdAt=datetime.utcnow().isoformat(),
                expiresAt=(datetime.utcnow() + timedelta(days=7)).isoformat()
            )
        
        completed_projects = await project_service.get_user_projects(user_id, status_filter=None)
        completed_count = len([p for p in completed_projects if p.get("status") == "completed"])
        
        # Build current profile snapshot
        skills_list = [skill.dict(by_alias=True) for skill in skill_graph.skills]
        current_profile = CurrentProfile(
            totalSkills=skill_graph.total_skills,
            verifiedSkills=skill_graph.verified_skills,
            inProgressSkills=skill_graph.in_progress_skills,
            completedProjects=completed_count,
            averageProficiency=self.calculate_average_proficiency(skills_list),
            skillCategories=self.categorize_skills(skills_list)
        )
        
        # Step 2: Get target internship requirements
        if not request.target_internship_ids:
            # No targets - return current profile only
            logger.info(f"No target internships specified for user: {user_id}")
            return SkillGapAnalysis(
                userId=user_id,
                analysisId=str(uuid4()),
                currentProfile=current_profile,
                skillGaps=[],
                prioritizedSkills=[],
                learningPath=[],
                estimatedTimeline="No target internships specified",
                confidenceScore=100.0,
                targetInternships=[],
                targetRoles=request.target_roles,
                createdAt=datetime.utcnow().isoformat(),
                expiresAt=(datetime.utcnow() + timedelta(days=7)).isoformat()
            )
        
        # Aggregate required skills across all target internships
        all_required_skills = {}
        
        for internship_id in request.target_internship_ids:
            internship = mock_store.get_internship(internship_id)
            if not internship:
                logger.warning(f"Internship not found: {internship_id}")
                continue
            
            for req_skill in internship.get("requiredSkills", []):
                skill_key = normalize_skill_name(req_skill["name"])
                
                if skill_key not in all_required_skills:
                    all_required_skills[skill_key] = {
                        "name": req_skill["name"],
                        "category": req_skill.get("category", "tool"),
                        "max_proficiency": req_skill["proficiencyLevel"],
                        "mandatory_count": 1 if req_skill.get("mandatory", False) else 0,
                        "total_count": 1,
                        "weight_sum": req_skill.get("weight", 1.0)
                    }
                else:
                    # Update with highest proficiency requirement
                    all_required_skills[skill_key]["max_proficiency"] = max(
                        all_required_skills[skill_key]["max_proficiency"],
                        req_skill["proficiencyLevel"]
                    )
                    all_required_skills[skill_key]["mandatory_count"] += (
                        1 if req_skill.get("mandatory", False) else 0
                    )
                    all_required_skills[skill_key]["total_count"] += 1
                    all_required_skills[skill_key]["weight_sum"] += req_skill.get("weight", 1.0)
        
        # Step 3: Calculate skill gaps
        skill_gaps = []
        user_skill_map = {normalize_skill_name(s.name): s for s in skill_graph.skills}
        
        for skill_key, req_data in all_required_skills.items():
            user_skill = user_skill_map.get(skill_key)
            current_prof = user_skill.proficiency_level if user_skill else 0
            target_prof = req_data["max_proficiency"]
            
            if current_prof < target_prof:
                gap_size = target_prof - current_prof
                
                # Calculate priority score
                priority_score = self.calculate_priority_score(
                    gap_size=gap_size,
                    mandatory_count=req_data["mandatory_count"],
                    total_count=req_data["total_count"],
                    weight_sum=req_data["weight_sum"]
                )
                
                # Estimate learning hours
                estimated_hours = self.estimate_learning_hours(
                    gap_size=gap_size,
                    category=req_data["category"],
                    learning_velocity=1.0  # Default velocity
                )
                
                skill_gap = SkillGap(
                    skillName=req_data["name"],
                    normalizedName=skill_key,
                    category=req_data["category"],
                    currentProficiency=current_prof,
                    targetProficiency=target_prof,
                    gapSize=gap_size,
                    priorityScore=priority_score,
                    impactOnEligibility=req_data["total_count"],
                    estimatedLearningHours=estimated_hours,
                    prerequisites=[],
                    relatedSkills=[]
                )
                skill_gaps.append(skill_gap)
        
        # Step 4: Sort gaps by priority
        skill_gaps.sort(key=lambda x: x.priority_score, reverse=True)
        
        # Step 5: Create learning path (topological sort)
        learning_path = self.topological_sort_skills(skill_gaps)
        
        # Step 6: Create prioritized skill list
        prioritized_skills = []
        for rank, skill_gap in enumerate(skill_gaps[:10], 1):
            prioritized_skill = PrioritizedSkill(
                skillName=skill_gap.skill_name,
                priorityRank=rank,
                priorityScore=skill_gap.priority_score,
                reasoning=f"Required by {skill_gap.impact_on_eligibility} internships with {skill_gap.gap_size} proficiency gap",
                internshipsUnlocked=skill_gap.impact_on_eligibility,
                suggestedProjects=[]
            )
            prioritized_skills.append(prioritized_skill)
        
        # Step 7: Estimate timeline
        total_hours = sum(gap.estimated_learning_hours for gap in skill_gaps)
        estimated_timeline = self.estimate_timeline_from_hours(total_hours)
        
        # Step 8: Calculate confidence score
        confidence_score = self.calculate_confidence_score(
            data_quality=completed_count,
            skill_count=len(skill_gaps),
            total_hours=total_hours
        )
        
        # Step 9: Create analysis
        analysis = SkillGapAnalysis(
            userId=user_id,
            analysisId=str(uuid4()),
            currentProfile=current_profile,
            skillGaps=skill_gaps,
            prioritizedSkills=prioritized_skills,
            learningPath=learning_path,
            estimatedTimeline=estimated_timeline,
            confidenceScore=confidence_score,
            targetInternships=request.target_internship_ids,
            targetRoles=request.target_roles,
            createdAt=datetime.utcnow().isoformat(),
            expiresAt=(datetime.utcnow() + timedelta(days=7)).isoformat()
        )
        
        # Save to store
        mock_store.save_skill_gap_analysis(user_id, analysis.dict(by_alias=True))
        
        logger.info(f"Profile analysis complete for user: {user_id} - {len(skill_gaps)} gaps found")
        return analysis
    
    @staticmethod
    def estimate_timeline_from_hours(total_hours: int) -> str:
        """Convert hours to human-readable timeline"""
        if total_hours < 40:
            return "1-2 weeks"
        elif total_hours < 80:
            return "3-4 weeks"
        elif total_hours < 160:
            return "2-3 months"
        elif total_hours < 320:
            return "3-6 months"
        else:
            return "6-12 months"
    
    @staticmethod
    def calculate_confidence_score(data_quality: int, skill_count: int, total_hours: int) -> float:
        """Calculate confidence score for analysis"""
        # Base confidence
        confidence = 70.0
        
        # Increase with more completed projects (data quality)
        confidence += min(data_quality * 5, 20)
        
        # Decrease with more skills (more uncertainty)
        confidence -= min(skill_count * 2, 20)
        
        # Decrease with longer timelines
        if total_hours > 200:
            confidence -= 10
        
        return max(min(confidence, 100.0), 0.0)
    
    async def get_skill_priorities(
        self,
        user_id: str,
        target_context: Optional[str] = None
    ) -> List[PrioritizedSkill]:
        """Get prioritized list of skills to learn"""
        # Get cached analysis or create new one
        cached = mock_store.get_skill_gap_analysis(user_id)
        
        if cached:
            # Check if expired
            expires_at = datetime.fromisoformat(cached["expiresAt"])
            if datetime.utcnow() < expires_at:
                return [PrioritizedSkill(**skill) for skill in cached["prioritizedSkills"]]
        
        # Create new analysis
        analysis = await self.analyze_profile(
            ProfileAnalysisRequest(
                userId=user_id,
                targetInternshipIds=[],
                includePredictions=False
            )
        )
        
        return analysis.prioritized_skills
    
    async def calculate_readiness_score(
        self,
        user_id: str,
        internship_id: str
    ) -> Dict[str, Any]:
        """Calculate career readiness for specific internship"""
        # Get skill graph
        skill_graph = await skill_service.get_skill_graph(user_id)
        if not skill_graph:
            return {
                "readinessScore": 0.0,
                "missingSkills": [],
                "readySkills": [],
                "estimatedTimeToReady": "Unknown"
            }
        
        # Get internship
        internship = mock_store.get_internship(internship_id)
        if not internship:
            return {
                "readinessScore": 0.0,
                "missingSkills": [],
                "readySkills": [],
                "estimatedTimeToReady": "Unknown"
            }
        
        # Calculate match using existing eligibility service
        from src.services.eligibility_service import eligibility_service
        
        # Use dict-based classification
        classification = eligibility_service.classify_internships_dict(
            skill_graph,
            [internship]
        )
        
        # Find the internship in results
        match_result = None
        for category in ["eligible", "almostEligible", "notEligible"]:
            if classification[category]:
                match_result = classification[category][0]
                break
        
        if not match_result:
            return {
                "readinessScore": 0.0,
                "missingSkills": [],
                "readySkills": [],
                "estimatedTimeToReady": "Unknown"
            }
        
        # Calculate readiness score (match score is readiness)
        readiness_score = match_result["matchScore"]
        
        # Get missing and ready skills
        missing_skills = match_result.get("skillGaps", [])
        ready_skills = match_result.get("matchedSkills", [])
        
        # Estimate time to ready
        total_gap_hours = sum(
            self.estimate_learning_hours(gap["gap"], "tool", 1.0)
            for gap in missing_skills
        )
        estimated_time = self.estimate_timeline_from_hours(total_gap_hours)
        
        return {
            "readinessScore": readiness_score,
            "missingSkills": missing_skills,
            "readySkills": ready_skills,
            "estimatedTimeToReady": estimated_time
        }


# Export singleton
skill_gap_intelligence_service = SkillGapIntelligenceService()
