"""Career Path Service - Generate progressive career roadmaps"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

from src.services.ai_service import ai_service
from src.services.skill_gap_intelligence_service import (
    skill_gap_intelligence_service,
    ProfileAnalysisRequest
)
from src.services.personalization_service import (
    personalization_service,
    PersonalizationContext
)
from src.services.prediction_service import prediction_service
from src.services.internship_mapping_service import internship_mapping_service
from src.utils.validation import normalize_skill_name
from src.utils.mock_store import mock_store

logger = logging.getLogger(__name__)


# Data Models
class CareerGoal(BaseModel):
    """Career goal definition"""
    target_role: str = Field(alias="targetRole")
    timeline_months: int = Field(alias="timelineMonths")
    
    class Config:
        populate_by_name = True


class CurrentPosition(BaseModel):
    """Student's current position"""
    verified_skills_count: int = Field(alias="verifiedSkillsCount")
    total_proficiency_score: float = Field(alias="totalProficiencyScore")
    completed_projects_count: int = Field(alias="completedProjectsCount")
    
    class Config:
        populate_by_name = True


class RoadmapMilestone(BaseModel):
    """Milestone in career roadmap"""
    milestone_id: str = Field(alias="milestoneId")
    title: str
    description: str
    order: int
    skills_to_acquire: List[str] = Field(alias="skillsToAcquire")
    target_projects: List[str] = Field(default_factory=list, alias="targetProjects")
    target_internships: List[str] = Field(default_factory=list, alias="targetInternships")
    estimated_weeks: int = Field(alias="estimatedWeeks")
    dependencies: List[str] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True


class CareerRoadmap(BaseModel):
    """Complete career roadmap"""
    roadmap_id: str = Field(alias="roadmapId")
    user_id: str = Field(alias="userId")
    target_role: str = Field(alias="targetRole")
    current_position: CurrentPosition = Field(alias="currentPosition")
    milestones: List[RoadmapMilestone]
    estimated_total_months: float = Field(alias="estimatedTotalMonths")
    created_at: str = Field(alias="createdAt")
    
    class Config:
        populate_by_name = True


class CareerPathService:
    """Service for generating progressive career roadmaps"""
    
    async def generate_roadmap(
        self,
        user_id: str,
        target_role: str,
        timeline_months: int = 6
    ) -> CareerRoadmap:
        """
        Generate complete career roadmap
        
        Creates 3-5 progressive milestones from current position to target role
        """
        logger.info(f"Generating roadmap for user {user_id}, role {target_role}")
        
        # Step 1: Get current position
        current_position = await self._get_current_position(user_id)
        
        # Step 2: Get skill gaps for target role
        skill_gaps = await self._get_skill_gaps_for_role(user_id, target_role)
        
        # Step 3: Generate milestone structure using AI
        milestones = await self._generate_milestones_with_ai(
            user_id,
            target_role,
            current_position,
            skill_gaps,
            timeline_months
        )
        
        # Step 4: Enrich milestones with projects and internships
        enriched_milestones = await self._enrich_milestones(
            user_id,
            milestones,
            skill_gaps
        )
        
        # Step 5: Validate dependencies (DAG check)
        validated_milestones = self._validate_dependencies(enriched_milestones)
        
        # Step 6: Calculate total timeline
        total_months = sum(m.estimated_weeks for m in validated_milestones) / 4.0
        
        # Step 7: Create roadmap
        roadmap = CareerRoadmap(
            roadmapId=str(uuid4()),
            userId=user_id,
            targetRole=target_role,
            currentPosition=current_position,
            milestones=validated_milestones,
            estimatedTotalMonths=round(total_months, 1),
            createdAt=datetime.utcnow().isoformat()
        )
        
        # Step 8: Cache roadmap (7 days)
        mock_store.save_career_roadmap(user_id, roadmap.dict(by_alias=True))
        
        logger.info(f"Roadmap generated: {len(validated_milestones)} milestones, {total_months:.1f} months")
        return roadmap
    
    async def _get_current_position(self, user_id: str) -> CurrentPosition:
        """Get student's current position snapshot"""
        from src.services.skill_service import skill_service
        from src.services.project_service import project_service
        
        # Get skill graph
        skill_graph = await skill_service.get_skill_graph(user_id)
        
        if not skill_graph:
            return CurrentPosition(
                verifiedSkillsCount=0,
                totalProficiencyScore=0.0,
                completedProjectsCount=0
            )
        
        # Get completed projects
        projects = await project_service.get_user_projects(user_id, status_filter=None)
        completed_count = len([p for p in projects if p.get("status") == "completed"])
        
        # Calculate total proficiency
        total_proficiency = sum(s.proficiency_level for s in skill_graph.skills)
        
        return CurrentPosition(
            verifiedSkillsCount=skill_graph.verified_skills,
            totalProficiencyScore=round(total_proficiency, 2),
            completedProjectsCount=completed_count
        )
    
    async def _get_skill_gaps_for_role(
        self,
        user_id: str,
        target_role: str
    ) -> List[Dict[str, Any]]:
        """Get skill gaps for target role"""
        # Get all internships matching role
        all_internships = mock_store.get_all_internships()
        role_internships = [
            i for i in all_internships
            if target_role.lower() in i.get("title", "").lower() or
               target_role.lower() in i.get("description", "").lower()
        ]
        
        if not role_internships:
            logger.warning(f"No internships found for role: {target_role}")
            return []
        
        # Get skill gap analysis
        internship_ids = [i["internshipId"] for i in role_internships[:5]]
        
        analysis = await skill_gap_intelligence_service.analyze_profile(
            ProfileAnalysisRequest(
                userId=user_id,
                targetInternshipIds=internship_ids,
                targetRoles=[target_role],
                includePredictions=False
            )
        )
        
        return [g.dict(by_alias=True) for g in analysis.skill_gaps]
    
    async def _generate_milestones_with_ai(
        self,
        user_id: str,
        target_role: str,
        current_position: CurrentPosition,
        skill_gaps: List[Dict[str, Any]],
        timeline_months: int
    ) -> List[RoadmapMilestone]:
        """Generate milestone structure using AI"""
        
        # Build prompt for AI
        skills_summary = ", ".join([g["skillName"] for g in skill_gaps[:10]])
        
        prompt = f"""Create a career roadmap with 3-5 progressive milestones.

Target Role: {target_role}
Timeline: {timeline_months} months
Current Position:
- Verified Skills: {current_position.verified_skills_count}
- Completed Projects: {current_position.completed_projects_count}

Skills to Learn: {skills_summary}

Return ONLY JSON (no markdown):
{{
  "milestones": [
    {{
      "title": "Foundation Skills",
      "description": "Build core technical foundation",
      "order": 1,
      "skillsToAcquire": ["Python", "Git"],
      "estimatedWeeks": 4
    }},
    {{
      "title": "Intermediate Development",
      "description": "Develop practical project experience",
      "order": 2,
      "skillsToAcquire": ["React", "APIs"],
      "estimatedWeeks": 6
    }},
    {{
      "title": "Advanced Specialization",
      "description": "Master role-specific skills",
      "order": 3,
      "skillsToAcquire": ["System Design", "Testing"],
      "estimatedWeeks": 6
    }}
  ]
}}

Create 3-5 milestones that progress from beginner to {target_role}. Return ONLY JSON."""

        try:
            response_text = await ai_service.call_ollama(prompt, temperature=0.7)
            
            if not response_text:
                # Fallback to template
                return self._generate_template_milestones(skill_gaps, timeline_months)
            
            # Clean response
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            import json
            result = json.loads(response_text)
            
            # Convert to RoadmapMilestone objects
            milestones = []
            for m_data in result.get("milestones", []):
                milestone = RoadmapMilestone(
                    milestoneId=str(uuid4()),
                    title=m_data.get("title", "Milestone"),
                    description=m_data.get("description", ""),
                    order=m_data.get("order", 1),
                    skillsToAcquire=m_data.get("skillsToAcquire", []),
                    estimatedWeeks=m_data.get("estimatedWeeks", 4),
                    dependencies=[]
                )
                milestones.append(milestone)
            
            return milestones
            
        except Exception as e:
            logger.error(f"AI milestone generation failed: {e}")
            return self._generate_template_milestones(skill_gaps, timeline_months)
    
    def _generate_template_milestones(
        self,
        skill_gaps: List[Dict[str, Any]],
        timeline_months: int
    ) -> List[RoadmapMilestone]:
        """Generate template milestones when AI fails"""
        
        # Sort skills by priority
        sorted_gaps = sorted(
            skill_gaps,
            key=lambda g: g.get("priorityScore", 0),
            reverse=True
        )
        
        # Split into 3 groups
        total_skills = len(sorted_gaps)
        group_size = max(total_skills // 3, 1)
        
        milestones = []
        
        # Milestone 1: Foundation (top priority skills)
        foundation_skills = [g["skillName"] for g in sorted_gaps[:group_size]]
        milestones.append(RoadmapMilestone(
            milestoneId=str(uuid4()),
            title="Foundation Skills",
            description="Build core technical foundation",
            order=1,
            skillsToAcquire=foundation_skills,
            estimatedWeeks=max(timeline_months // 3, 2),
            dependencies=[]
        ))
        
        # Milestone 2: Intermediate (middle priority)
        intermediate_skills = [g["skillName"] for g in sorted_gaps[group_size:group_size*2]]
        if intermediate_skills:
            milestones.append(RoadmapMilestone(
                milestoneId=str(uuid4()),
                title="Intermediate Development",
                description="Develop practical project experience",
                order=2,
                skillsToAcquire=intermediate_skills,
                estimatedWeeks=max(timeline_months // 3, 2),
                dependencies=[milestones[0].milestone_id]
            ))
        
        # Milestone 3: Advanced (remaining skills)
        advanced_skills = [g["skillName"] for g in sorted_gaps[group_size*2:]]
        if advanced_skills:
            milestones.append(RoadmapMilestone(
                milestoneId=str(uuid4()),
                title="Advanced Specialization",
                description="Master role-specific skills",
                order=3,
                skillsToAcquire=advanced_skills,
                estimatedWeeks=max(timeline_months // 3, 2),
                dependencies=[milestones[-1].milestone_id]
            ))
        
        return milestones
    
    async def _enrich_milestones(
        self,
        user_id: str,
        milestones: List[RoadmapMilestone],
        skill_gaps: List[Dict[str, Any]]
    ) -> List[RoadmapMilestone]:
        """Enrich milestones with project suggestions and internship targets"""
        
        enriched = []
        
        for milestone in milestones:
            # Get project suggestions for milestone skills
            try:
                # Build context for personalization
                from src.services.skill_service import skill_service
                
                skill_graph = await skill_service.get_skill_graph(user_id)
                current_proficiency = {}
                if skill_graph:
                    current_proficiency = {
                        normalize_skill_name(s.name): s.proficiency_level
                        for s in skill_graph.skills
                    }
                
                # Get learning velocity
                learning_velocity = await personalization_service.calculate_learning_velocity(user_id)
                
                # Filter skill gaps for this milestone
                milestone_gaps = [
                    g for g in skill_gaps
                    if g["skillName"] in milestone.skills_to_acquire
                ]
                
                if milestone_gaps:
                    context = PersonalizationContext(
                        userId=user_id,
                        skillGaps=milestone_gaps,
                        currentProficiencyLevels=current_proficiency,
                        careerGoals=[],
                        targetRoles=[],
                        learningVelocity=learning_velocity,
                        completedProjects=[],
                        timeAvailablePerWeek=14
                    )
                    
                    # Get top 2 project suggestions
                    suggestions = await personalization_service.suggest_projects(context, limit=2)
                    milestone.target_projects = [s.project_id for s in suggestions]
                
            except Exception as e:
                logger.warning(f"Could not enrich milestone with projects: {e}")
            
            # Get target internships for milestone skills
            try:
                # Find internships that require these skills
                all_internships = mock_store.get_all_internships()
                
                matching_internships = []
                for internship in all_internships:
                    required_skills = [
                        normalize_skill_name(s["name"])
                        for s in internship.get("requiredSkills", [])
                    ]
                    milestone_skill_keys = [
                        normalize_skill_name(s)
                        for s in milestone.skills_to_acquire
                    ]
                    
                    # Check overlap
                    overlap = set(required_skills) & set(milestone_skill_keys)
                    if overlap:
                        matching_internships.append(internship["internshipId"])
                
                milestone.target_internships = matching_internships[:3]
                
            except Exception as e:
                logger.warning(f"Could not enrich milestone with internships: {e}")
            
            enriched.append(milestone)
        
        return enriched
    
    def _validate_dependencies(
        self,
        milestones: List[RoadmapMilestone]
    ) -> List[RoadmapMilestone]:
        """Validate milestone dependencies form a valid DAG (no cycles)"""
        
        # Build adjacency list
        graph = {m.milestone_id: m.dependencies for m in milestones}
        
        # Check for cycles using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        # Check each milestone
        for milestone in milestones:
            if milestone.milestone_id not in visited:
                if has_cycle(milestone.milestone_id):
                    logger.warning(f"Cycle detected in milestone dependencies")
                    # Break cycle by removing dependencies
                    for m in milestones:
                        m.dependencies = []
                    # Re-add simple sequential dependencies
                    for i, m in enumerate(milestones):
                        if i > 0:
                            m.dependencies = [milestones[i-1].milestone_id]
                    break
        
        return milestones
    
    async def update_roadmap_progress(
        self,
        roadmap_id: str,
        milestone_id: str,
        status: str,
        notes: Optional[str] = None
    ) -> CareerRoadmap:
        """
        Update progress on a specific milestone
        
        Args:
            roadmap_id: ID of the roadmap
            milestone_id: ID of the milestone to update
            status: New status ("not_started", "in_progress", "completed")
            notes: Optional progress notes
        
        Returns updated roadmap with recalculated progress
        """
        logger.info(f"Updating roadmap {roadmap_id}, milestone {milestone_id} to {status}")
        
        # Get existing roadmap
        roadmap_data = mock_store.get_career_roadmap(roadmap_id)
        if not roadmap_data:
            raise ValueError(f"Roadmap not found: {roadmap_id}")
        
        # Find and update milestone
        milestones = roadmap_data.get("milestones", [])
        milestone_found = False
        
        for milestone in milestones:
            if milestone.get("milestoneId") == milestone_id:
                milestone["status"] = status
                milestone["lastUpdated"] = datetime.utcnow().isoformat()
                
                if status == "completed":
                    milestone["completedAt"] = datetime.utcnow().isoformat()
                
                if notes:
                    if "progressNotes" not in milestone:
                        milestone["progressNotes"] = []
                    milestone["progressNotes"].append({
                        "note": notes,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                
                milestone_found = True
                break
        
        if not milestone_found:
            raise ValueError(f"Milestone not found: {milestone_id}")
        
        # Recalculate overall progress
        total_milestones = len(milestones)
        completed_milestones = len([m for m in milestones if m.get("status") == "completed"])
        progress_percentage = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
        
        # Update roadmap
        roadmap_data["progressPercentage"] = round(progress_percentage, 2)
        roadmap_data["completedMilestones"] = completed_milestones
        roadmap_data["lastUpdated"] = datetime.utcnow().isoformat()
        
        # Save updated roadmap
        mock_store.save_career_roadmap(roadmap_id, roadmap_data)
        
        logger.info(f"Roadmap progress updated: {progress_percentage}% complete")
        return CareerRoadmap(**roadmap_data)
    
    async def suggest_next_steps(
        self,
        user_id: str,
        roadmap_id: str
    ) -> Dict[str, Any]:
        """
        Suggest next actionable steps based on current progress
        
        Returns prioritized list of next steps with reasoning
        """
        logger.info(f"Generating next steps for user {user_id}, roadmap {roadmap_id}")
        
        # Get roadmap
        roadmap_data = mock_store.get_career_roadmap(roadmap_id)
        if not roadmap_data:
            raise ValueError(f"Roadmap not found: {roadmap_id}")
        
        if roadmap_data.get("userId") != user_id:
            raise ValueError("Roadmap does not belong to user")
        
        milestones = roadmap_data.get("milestones", [])
        
        # Find next incomplete milestone
        next_milestone = None
        for milestone in milestones:
            if milestone.get("status") != "completed":
                next_milestone = milestone
                break
        
        if not next_milestone:
            return {
                "nextSteps": [],
                "message": "Congratulations! You've completed all milestones in this roadmap.",
                "roadmapComplete": True
            }
        
        # Get current user skills
        from src.services.skill_service import skill_service
        skill_graph = await skill_service.get_skill_graph(user_id)
        current_skills = {normalize_skill_name(s.name): s.proficiency_level for s in skill_graph.skills} if skill_graph else {}
        
        # Generate actionable steps
        next_steps = []
        
        # Step 1: Skills to learn
        target_skills = next_milestone.get("skillsToAcquire", [])
        skills_to_learn = []
        
        for skill in target_skills:
            skill_key = normalize_skill_name(skill)
            current_prof = current_skills.get(skill_key, 0)
            
            if current_prof < 70:  # Threshold for milestone completion
                skills_to_learn.append({
                    "skill": skill,
                    "currentProficiency": current_prof,
                    "targetProficiency": 70,
                    "gap": 70 - current_prof
                })
        
        if skills_to_learn:
            next_steps.append({
                "type": "learn_skills",
                "priority": "high",
                "title": f"Learn {len(skills_to_learn)} required skills",
                "skills": skills_to_learn,
                "estimatedHours": sum(s["gap"] * 1.5 for s in skills_to_learn)
            })
        
        # Step 2: Projects to complete
        suggested_projects = next_milestone.get("targetProjects", [])
        if suggested_projects:
            next_steps.append({
                "type": "complete_projects",
                "priority": "high",
                "title": f"Complete {len(suggested_projects)} recommended projects",
                "projects": suggested_projects,
                "estimatedHours": next_milestone.get("estimatedWeeks", 4) * 10
            })
        
        # Step 3: Internships to apply
        target_internships = next_milestone.get("targetInternships", [])
        if target_internships:
            next_steps.append({
                "type": "apply_internships",
                "priority": "medium",
                "title": f"Apply to {len(target_internships)} target internships",
                "internships": target_internships
            })
        
        # Generate AI-powered recommendations
        try:
            prompt = f"""Generate 3 specific, actionable next steps for a student working on this career milestone.

Milestone: {next_milestone.get('title', 'Career Milestone')}
Description: {next_milestone.get('description', '')}
Skills Needed: {', '.join(target_skills)}
Current Progress: {next_milestone.get('status', 'not_started')}

Student Context:
- Current skills: {len(current_skills)} skills
- Skills to learn: {len(skills_to_learn)} skills
- Projects suggested: {len(suggested_projects)}

Provide 3 concrete, actionable steps (1-2 sentences each) that the student should take this week.
Focus on immediate, practical actions."""

            ai_suggestions = await ai_service.call_ollama(prompt, temperature=0.7)
            
            if ai_suggestions:
                next_steps.append({
                    "type": "ai_recommendations",
                    "priority": "medium",
                    "title": "AI-Powered Recommendations",
                    "recommendations": ai_suggestions.strip()
                })
        
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {e}")
        
        return {
            "nextSteps": next_steps,
            "currentMilestone": next_milestone,
            "roadmapComplete": False,
            "overallProgress": roadmap_data.get("progressPercentage", 0)
        }
    
    def estimate_timeline(
        self,
        milestones: List[Dict[str, Any]],
        learning_velocity: float = 1.0
    ) -> Dict[str, Any]:
        """
        Estimate timeline for completing all milestones
        
        Args:
            milestones: List of milestone dictionaries
            learning_velocity: User's learning speed multiplier (default 1.0)
        
        Returns timeline breakdown with dates and durations
        """
        logger.info(f"Estimating timeline for {len(milestones)} milestones")
        
        total_hours = 0
        milestone_timelines = []
        current_date = datetime.utcnow()
        
        for milestone in milestones:
            # Get estimated duration
            duration_weeks = milestone.get("estimatedWeeks", 4)
            duration_hours = duration_weeks * 10  # 10 hours per week
            
            # Adjust for learning velocity
            adjusted_hours = duration_hours / learning_velocity
            
            # Calculate weeks needed
            weeks_needed = adjusted_hours / 10
            
            # Calculate end date
            end_date = current_date + timedelta(weeks=weeks_needed)
            
            milestone_timelines.append({
                "milestoneId": milestone.get("milestoneId"),
                "title": milestone.get("title"),
                "estimatedHours": int(adjusted_hours),
                "estimatedWeeks": round(weeks_needed, 1),
                "startDate": current_date.isoformat(),
                "endDate": end_date.isoformat()
            })
            
            total_hours += adjusted_hours
            current_date = end_date
        
        # Calculate total timeline
        total_weeks = total_hours / 10
        total_months = total_weeks / 4
        
        if total_months < 1:
            timeline_summary = f"{int(total_weeks)} weeks"
        elif total_months < 12:
            timeline_summary = f"{int(total_months)} months"
        else:
            years = int(total_months / 12)
            remaining_months = int(total_months % 12)
            timeline_summary = f"{years} year{'s' if years > 1 else ''}"
            if remaining_months > 0:
                timeline_summary += f" {remaining_months} months"
        
        return {
            "totalHours": int(total_hours),
            "totalWeeks": round(total_weeks, 1),
            "totalMonths": round(total_months, 1),
            "timelineSummary": timeline_summary,
            "estimatedCompletionDate": current_date.isoformat(),
            "milestoneTimelines": milestone_timelines
        }


# Add storage methods to mock_store
def save_career_roadmap(user_id: str, roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
    """Save career roadmap"""
    if not hasattr(mock_store, '_career_roadmaps'):
        mock_store._career_roadmaps = {}
    
    roadmap_data["expiresAt"] = (datetime.utcnow() + timedelta(days=7)).isoformat()
    mock_store._career_roadmaps[user_id] = roadmap_data
    return roadmap_data


def get_career_roadmap(user_id: str) -> Optional[Dict[str, Any]]:
    """Get cached career roadmap"""
    if not hasattr(mock_store, '_career_roadmaps'):
        return None
    
    cached = mock_store._career_roadmaps.get(user_id)
    
    if cached:
        # Check expiration
        expires_at = datetime.fromisoformat(cached["expiresAt"])
        if datetime.utcnow() < expires_at:
            return cached
        else:
            del mock_store._career_roadmaps[user_id]
    
    return None


# Monkey-patch mock_store
mock_store.save_career_roadmap = save_career_roadmap
mock_store.get_career_roadmap = get_career_roadmap


# Export singleton
career_path_service = CareerPathService()
