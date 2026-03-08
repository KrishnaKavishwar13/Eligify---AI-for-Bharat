"""Personalization Service - Smart project recommendations with AI integration"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

from src.services.ai_service import ai_service
from src.services.skill_gap_intelligence_service import skill_gap_intelligence_service
from src.services.project_service import project_service
from src.services.internship_mapping_service import internship_mapping_service
from src.services.skill_service import skill_service
from src.services.eligibility_service import eligibility_service
from src.utils.validation import normalize_skill_name
from src.utils.mock_store import mock_store

logger = logging.getLogger(__name__)


# Data Models
class LearningVelocityMetrics(BaseModel):
    """Metrics for learning velocity calculation"""
    projects_completed_last_30_days: int = Field(alias="projectsCompletedLast30Days")
    skills_gained_last_30_days: int = Field(alias="skillsGainedLast30Days")
    average_project_completion_time: float = Field(alias="averageProjectCompletionTime")
    skill_acquisition_rate: float = Field(alias="skillAcquisitionRate")
    consistency_score: float = Field(alias="consistencyScore", ge=0, le=100)
    acceleration_trend: str = Field(alias="accelerationTrend")  # "increasing", "stable", "decreasing"

    class Config:
        populate_by_name = True


class PersonalizationContext(BaseModel):
    """Context for personalized recommendations"""
    user_id: str = Field(alias="userId")
    skill_gaps: List[Dict[str, Any]] = Field(alias="skillGaps")
    current_proficiency_levels: Dict[str, int] = Field(alias="currentProficiencyLevels")
    career_goals: List[str] = Field(alias="careerGoals")
    target_roles: List[str] = Field(alias="targetRoles")
    learning_velocity: LearningVelocityMetrics = Field(alias="learningVelocity")
    completed_projects: List[str] = Field(alias="completedProjects")
    time_available_per_week: int = Field(alias="timeAvailablePerWeek")

    class Config:
        populate_by_name = True


class PersonalizedProjectSuggestion(BaseModel):
    """Personalized project suggestion with reasoning"""
    project_id: str = Field(alias="projectId")
    title: str
    description: str
    difficulty_level: str = Field(alias="difficultyLevel")
    target_skills: List[str] = Field(alias="targetSkills")
    estimated_hours: int = Field(alias="estimatedHours")
    relevance_score: float = Field(alias="relevanceScore", ge=0, le=100)
    internships_unlocked: List[str] = Field(alias="internshipsUnlocked")
    reasoning: str
    prerequisites: List[str] = []

    class Config:
        populate_by_name = True


class PersonalizationService:
    """Service for smart, personalized project recommendations"""
    
    async def calculate_learning_velocity(self, user_id: str) -> LearningVelocityMetrics:
        """
        Calculate user's learning velocity from historical data
        
        Returns metrics tracking learning speed and consistency
        """
        logger.info(f"Calculating learning velocity for user: {user_id}")
        
        # Get user's project history
        all_projects = await project_service.get_user_projects(user_id, status_filter=None)
        completed_projects = [p for p in all_projects if p.get("status") == "completed"]
        
        # Get skill graph for skill verification history
        skill_graph = await skill_service.get_skill_graph(user_id)
        
        # If insufficient data, return platform averages
        if len(completed_projects) < 2:
            logger.info(f"Insufficient data for user {user_id}, using platform averages")
            return LearningVelocityMetrics(
                projectsCompletedLast30Days=0,
                skillsGainedLast30Days=0,
                averageProjectCompletionTime=14.0,  # 2 weeks average
                skillAcquisitionRate=2.0,  # 2 skills per month
                consistencyScore=50.0,
                accelerationTrend="stable"
            )
        
        # Calculate metrics from last 30 days
        from datetime import timedelta
        now = datetime.utcnow()
        thirty_days_ago = now - timedelta(days=30)
        
        recent_completions = [
            p for p in completed_projects
            if p.get("completedAt") and datetime.fromisoformat(p["completedAt"]) > thirty_days_ago
        ]
        
        # Calculate average completion time
        completion_times = []
        for project in completed_projects:
            if project.get("acceptedAt") and project.get("completedAt"):
                accepted = datetime.fromisoformat(project["acceptedAt"])
                completed = datetime.fromisoformat(project["completedAt"])
                days = (completed - accepted).days
                if days > 0:
                    completion_times.append(days)
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 14.0
        
        # Calculate skill acquisition rate (skills verified in last 30 days)
        verified_skills_count = skill_graph.verified_skills if skill_graph else 0
        skill_acquisition_rate = verified_skills_count / max(len(completed_projects), 1)
        
        # Calculate consistency score (based on regular activity)
        consistency_score = min(len(recent_completions) * 25, 100.0)
        
        # Determine acceleration trend
        if len(completed_projects) >= 4:
            recent_half = completed_projects[-len(completed_projects)//2:]
            older_half = completed_projects[:len(completed_projects)//2]
            
            recent_avg = len(recent_half) / max(1, len(recent_half))
            older_avg = len(older_half) / max(1, len(older_half))
            
            if recent_avg > older_avg * 1.2:
                acceleration_trend = "increasing"
            elif recent_avg < older_avg * 0.8:
                acceleration_trend = "decreasing"
            else:
                acceleration_trend = "stable"
        else:
            acceleration_trend = "stable"
        
        return LearningVelocityMetrics(
            projectsCompletedLast30Days=len(recent_completions),
            skillsGainedLast30Days=int(skill_acquisition_rate * 30),
            averageProjectCompletionTime=round(avg_completion_time, 1),
            skillAcquisitionRate=round(skill_acquisition_rate, 2),
            consistencyScore=round(consistency_score, 2),
            accelerationTrend=acceleration_trend
        )
    
    def calculate_relevance_score(
        self,
        project: Dict[str, Any],
        skill_gaps: List[Dict[str, Any]],
        context: PersonalizationContext
    ) -> float:
        """
        Calculate relevance score for a project (0-100)
        
        Scoring breakdown:
        - Skill gap coverage: 0-40 points
        - Difficulty match: 0-20 points
        - Career goal alignment: 0-20 points
        - Learning velocity fit: 0-10 points
        - Time availability fit: 0-10 points
        """
        score = 0.0
        
        # 1. Skill gap coverage (0-40 points)
        project_skills = set(normalize_skill_name(s) for s in project.get("targetSkills", []))
        gap_skills = set(normalize_skill_name(g["skillName"]) for g in skill_gaps)
        
        if gap_skills:
            coverage = len(project_skills & gap_skills) / len(gap_skills)
            score += coverage * 40
        
        # 2. Difficulty match (0-20 points)
        project_difficulty = project.get("difficulty", "intermediate")
        
        # Calculate user's average proficiency for project skills
        avg_proficiency = 0
        skill_count = 0
        for skill in project.get("targetSkills", []):
            skill_key = normalize_skill_name(skill)
            if skill_key in context.current_proficiency_levels:
                avg_proficiency += context.current_proficiency_levels[skill_key]
                skill_count += 1
        
        if skill_count > 0:
            avg_proficiency = avg_proficiency / skill_count
        
        # Match difficulty to proficiency
        expected_difficulty = self.match_difficulty(project, avg_proficiency)
        
        if expected_difficulty == project_difficulty:
            score += 20  # Perfect match
        elif (expected_difficulty == "beginner" and project_difficulty == "intermediate") or \
             (expected_difficulty == "intermediate" and project_difficulty == "beginner") or \
             (expected_difficulty == "intermediate" and project_difficulty == "advanced") or \
             (expected_difficulty == "advanced" and project_difficulty == "intermediate"):
            score += 10  # Close match
        else:
            score += 5  # Mismatch but still valuable
        
        # 3. Career goal alignment (0-20 points)
        # Check if project skills align with career goals
        if context.career_goals or context.target_roles:
            # Simple heuristic: if project addresses high-priority gaps, it aligns with goals
            high_priority_gaps = [g for g in skill_gaps if g.get("priorityScore", 0) > 70]
            high_priority_skills = set(normalize_skill_name(g["skillName"]) for g in high_priority_gaps)
            
            if high_priority_skills:
                alignment = len(project_skills & high_priority_skills) / len(high_priority_skills)
                score += alignment * 20
            else:
                score += 10  # Default moderate alignment
        else:
            score += 10  # No specific goals, moderate score
        
        # 4. Learning velocity fit (0-10 points)
        project_hours = project.get("estimatedHours", 40)
        avg_completion_days = context.learning_velocity.average_project_completion_time
        
        # Estimate if project fits user's pace
        expected_hours_per_day = project_hours / max(avg_completion_days, 1)
        
        if 2 <= expected_hours_per_day <= 6:
            score += 10  # Good fit
        elif 1 <= expected_hours_per_day <= 8:
            score += 7  # Acceptable fit
        else:
            score += 4  # Challenging fit
        
        # 5. Time availability fit (0-10 points)
        hours_per_week = context.time_available_per_week
        weeks_needed = project_hours / max(hours_per_week, 1)
        
        if weeks_needed <= 4:
            score += 10  # Fits well in timeline
        elif weeks_needed <= 8:
            score += 7  # Moderate timeline
        else:
            score += 4  # Long timeline
        
        return min(round(score, 2), 100.0)
    
    def match_difficulty(self, project: Dict[str, Any], user_proficiency: float) -> str:
        """
        Match project difficulty to user's proficiency level
        
        Returns: "beginner", "intermediate", or "advanced"
        """
        if user_proficiency < 30:
            return "beginner"
        elif user_proficiency < 70:
            return "intermediate"
        else:
            return "advanced"
    
    async def suggest_projects(
        self,
        context: PersonalizationContext,
        limit: int = 5
    ) -> List[PersonalizedProjectSuggestion]:
        """
        Generate personalized project suggestions
        
        Returns top N project suggestions ranked by relevance
        """
        logger.info(f"Generating project suggestions for user: {context.user_id}")
        
        suggestions = []
        
        # Get top priority skills to address (top 5)
        priority_skills = sorted(
            context.skill_gaps,
            key=lambda g: g.get("priorityScore", 0),
            reverse=True
        )[:5]
        
        if not priority_skills:
            logger.warning(f"No skill gaps found for user: {context.user_id}")
            return []
        
        # Generate projects for each priority skill
        for skill_gap in priority_skills:
            skill_name = skill_gap["skillName"]
            
            # Determine appropriate difficulty level
            current_proficiency = context.current_proficiency_levels.get(
                normalize_skill_name(skill_name),
                0
            )
            
            if current_proficiency < 30:
                difficulty = "beginner"
            elif current_proficiency < 70:
                difficulty = "intermediate"
            else:
                difficulty = "advanced"
            
            # Generate project using AI
            try:
                project = await ai_service.generate_project(
                    target_skills=[skill_name],
                    student_level=difficulty,
                    user_context={
                        "completed_projects": context.completed_projects,
                        "career_goals": context.career_goals,
                        "time_availability": f"{context.time_available_per_week} hours/week"
                    }
                )
                
                if not project:
                    logger.warning(f"Failed to generate project for skill: {skill_name}")
                    continue
                
                # Add project ID if not present
                if "projectId" not in project:
                    project["projectId"] = str(uuid4())
                
                # Calculate relevance score
                relevance_score = self.calculate_relevance_score(
                    project,
                    context.skill_gaps,
                    context
                )
                
                # Calculate internships unlocked
                internships_unlocked = await self.calculate_internships_unlocked(
                    context.user_id,
                    [skill_name],
                    context.current_proficiency_levels
                )
                
                # Adjust estimated hours based on learning velocity
                base_hours = project.get("estimatedHours", 40)
                adjusted_hours = self.adjust_hours_for_velocity(
                    base_hours,
                    context.learning_velocity.average_project_completion_time
                )
                
                # Generate reasoning using AI
                reasoning = await self.generate_reasoning(
                    project,
                    skill_gap,
                    context,
                    len(internships_unlocked)
                )
                
                # Create suggestion
                suggestion = PersonalizedProjectSuggestion(
                    projectId=project["projectId"],
                    title=project.get("title", "Learning Project"),
                    description=project.get("description", ""),
                    difficultyLevel=difficulty,
                    targetSkills=[skill_name],
                    estimatedHours=adjusted_hours,
                    relevanceScore=relevance_score,
                    internshipsUnlocked=internships_unlocked,
                    reasoning=reasoning,
                    prerequisites=skill_gap.get("prerequisites", [])
                )
                
                suggestions.append(suggestion)
                
                # Cache the generated project
                project_data = project.copy()
                project_data.update({
                    "userId": context.user_id,
                    "status": "suggested",
                    "createdAt": datetime.utcnow().isoformat(),
                    "updatedAt": datetime.utcnow().isoformat()
                })
                mock_store.save_project(project_data)
                
            except Exception as e:
                logger.error(f"Error generating project for skill {skill_name}: {e}")
                continue
        
        # Sort by relevance score and return top N
        suggestions.sort(key=lambda s: s.relevance_score, reverse=True)
        
        # Cache suggestions
        cache_data = {
            "userId": context.user_id,
            "suggestions": [s.dict(by_alias=True) for s in suggestions[:limit]],
            "createdAt": datetime.utcnow().isoformat(),
            "expiresAt": (datetime.utcnow().timestamp() + 86400)  # 24 hours
        }
        mock_store.save_personalized_suggestions(context.user_id, cache_data)
        
        logger.info(f"Generated {len(suggestions[:limit])} suggestions for user: {context.user_id}")
        return suggestions[:limit]
    
    async def calculate_internships_unlocked(
        self,
        user_id: str,
        skills_to_add: List[str],
        current_proficiency_levels: Dict[str, int]
    ) -> List[str]:
        """
        Calculate which internships would become eligible after learning skills
        
        Returns list of internship IDs
        """
        # Get current skill graph
        skill_graph = await skill_service.get_skill_graph(user_id)
        if not skill_graph:
            return []
        
        # Get all internships
        all_internships = mock_store.get_all_internships()
        
        # Calculate current eligibility
        current_classification = eligibility_service.classify_internships_dict(
            skill_graph,
            all_internships
        )
        current_eligible_ids = set(i["internshipId"] for i in current_classification["eligible"])
        
        # Simulate adding skills at 70% proficiency
        from src.models.skill import SkillNode, SkillStatus, SkillCategory, SkillSource, SkillGraph
        
        simulated_skills = skill_graph.skills.copy()
        
        for skill_name in skills_to_add:
            skill_key = normalize_skill_name(skill_name)
            
            # Check if skill already exists
            existing_skill = next(
                (s for s in simulated_skills if normalize_skill_name(s.name) == skill_key),
                None
            )
            
            if existing_skill:
                # Update proficiency to 70 if lower
                if existing_skill.proficiency_level < 70:
                    existing_skill.proficiency_level = 70
                    existing_skill.verified = True
            else:
                # Add new skill
                new_skill = SkillNode(
                    skillId=str(uuid4()),
                    name=skill_name,
                    normalizedName=skill_key,
                    category=SkillCategory.TOOL,
                    status=SkillStatus.VERIFIED,
                    proficiencyLevel=70,
                    verified=True,
                    source=SkillSource.MANUAL,
                    relatedSkills=[],
                    prerequisites=[],
                    addedAt=datetime.utcnow().isoformat(),
                    lastUpdatedAt=datetime.utcnow().isoformat()
                )
                simulated_skills.append(new_skill)
        
        # Create simulated skill graph
        simulated_graph = SkillGraph(
            userId=user_id,
            skills=simulated_skills,
            totalSkills=len(simulated_skills),
            verifiedSkills=len([s for s in simulated_skills if s.verified]),
            inProgressSkills=len([s for s in simulated_skills if s.status == SkillStatus.IN_PROGRESS]),
            lastUpdated=datetime.utcnow().isoformat()
        )
        
        # Calculate projected eligibility
        projected_classification = eligibility_service.classify_internships_dict(
            simulated_graph,
            all_internships
        )
        projected_eligible_ids = set(i["internshipId"] for i in projected_classification["eligible"])
        
        # Return newly unlocked internships
        newly_unlocked = list(projected_eligible_ids - current_eligible_ids)
        return newly_unlocked
    
    def adjust_hours_for_velocity(
        self,
        base_hours: int,
        avg_completion_days: float
    ) -> int:
        """Adjust estimated hours based on user's learning velocity"""
        # If user completes projects faster than average, reduce hours
        # If slower, increase hours
        
        platform_avg_days = 14.0  # 2 weeks
        
        if avg_completion_days < platform_avg_days:
            # Faster learner - reduce estimate
            factor = avg_completion_days / platform_avg_days
            adjusted = int(base_hours * factor)
        else:
            # Slower learner - increase estimate
            factor = avg_completion_days / platform_avg_days
            adjusted = int(base_hours * factor)
        
        return max(adjusted, 1)
    
    async def generate_reasoning(
        self,
        project: Dict[str, Any],
        skill_gap: Dict[str, Any],
        context: PersonalizationContext,
        internships_unlocked_count: int
    ) -> str:
        """Generate natural language reasoning for project suggestion"""
        
        prompt = f"""Generate a brief, encouraging explanation (2-3 sentences) for why this project is recommended.

Student Context:
- Skill gap: {skill_gap['skillName']} (current: {skill_gap.get('currentProficiency', 0)}%, target: {skill_gap.get('targetProficiency', 100)}%)
- Career goals: {', '.join(context.career_goals) if context.career_goals else 'General skill development'}
- Completed projects: {len(context.completed_projects)}

Project:
- Title: {project.get('title', 'Learning Project')}
- Skills: {', '.join(project.get('targetSkills', []))}
- Difficulty: {project.get('difficulty', 'intermediate')}

Impact:
- Unlocks {internships_unlocked_count} new internship opportunities

Write in a natural, encouraging tone. Focus on the learning value and career impact."""

        try:
            reasoning_text = await ai_service.call_ollama(prompt, temperature=0.7)
            
            if reasoning_text:
                # Clean up the response
                reasoning_text = reasoning_text.strip()
                # Remove any JSON formatting if present
                if reasoning_text.startswith('{') or reasoning_text.startswith('['):
                    # Fallback to template
                    reasoning_text = None
            
            if not reasoning_text:
                # Fallback template
                reasoning_text = f"This project will help you master {skill_gap['skillName']}, " \
                               f"closing a {skill_gap.get('gapSize', 0)}-point skill gap. " \
                               f"Completing it could unlock {internships_unlocked_count} new internship opportunities."
            
            return reasoning_text
            
        except Exception as e:
            logger.error(f"Error generating reasoning: {e}")
            # Fallback template
            return f"This project addresses your {skill_gap['skillName']} skill gap and " \
                   f"could unlock {internships_unlocked_count} new opportunities."
    
    async def rank_projects(
        self,
        projects: List[Dict[str, Any]],
        context: PersonalizationContext
    ) -> List[PersonalizedProjectSuggestion]:
        """
        Rank existing projects by relevance to user's goals and skill gaps
        
        Takes a list of existing projects and returns them ranked by relevance score
        """
        logger.info(f"Ranking {len(projects)} projects for user: {context.user_id}")
        
        ranked_suggestions = []
        
        for project in projects:
            try:
                # Calculate relevance score
                relevance_score = self.calculate_relevance_score(
                    project,
                    context.skill_gaps,
                    context
                )
                
                # Calculate internships unlocked
                project_skills = project.get("targetSkills", [])
                internships_unlocked = await self.calculate_internships_unlocked(
                    context.user_id,
                    project_skills,
                    context.current_proficiency_levels
                )
                
                # Adjust estimated hours based on learning velocity
                base_hours = project.get("estimatedHours", 40)
                adjusted_hours = self.adjust_hours_for_velocity(
                    base_hours,
                    context.learning_velocity.average_project_completion_time
                )
                
                # Determine difficulty match
                avg_proficiency = 0
                skill_count = 0
                for skill in project_skills:
                    skill_key = normalize_skill_name(skill)
                    if skill_key in context.current_proficiency_levels:
                        avg_proficiency += context.current_proficiency_levels[skill_key]
                        skill_count += 1
                
                if skill_count > 0:
                    avg_proficiency = avg_proficiency / skill_count
                
                expected_difficulty = self.match_difficulty(project, avg_proficiency)
                actual_difficulty = project.get("difficulty", "intermediate")
                
                if expected_difficulty == actual_difficulty:
                    difficulty_match = "perfect"
                elif abs(["beginner", "intermediate", "advanced"].index(expected_difficulty) - 
                        ["beginner", "intermediate", "advanced"].index(actual_difficulty)) == 1:
                    difficulty_match = "close"
                else:
                    difficulty_match = "mismatch"
                
                # Generate reasoning
                reasoning = f"This project addresses {len(project_skills)} of your target skills " \
                           f"with a relevance score of {relevance_score:.1f}/100. " \
                           f"It could unlock {len(internships_unlocked)} new internship opportunities."
                
                # Create suggestion
                suggestion = PersonalizedProjectSuggestion(
                    projectId=project.get("projectId", str(uuid4())),
                    title=project.get("title", "Project"),
                    description=project.get("description", ""),
                    difficultyLevel=actual_difficulty,
                    targetSkills=project_skills,
                    estimatedHours=adjusted_hours,
                    relevanceScore=relevance_score,
                    internshipsUnlocked=internships_unlocked,
                    reasoning=reasoning,
                    prerequisites=project.get("prerequisites", [])
                )
                
                ranked_suggestions.append(suggestion)
                
            except Exception as e:
                logger.error(f"Error ranking project {project.get('projectId', 'unknown')}: {e}")
                continue
        
        # Sort by relevance score descending
        ranked_suggestions.sort(key=lambda s: s.relevance_score, reverse=True)
        
        logger.info(f"Ranked {len(ranked_suggestions)} projects for user: {context.user_id}")
        return ranked_suggestions
    
    async def adapt_project_difficulty(
        self,
        project: Dict[str, Any],
        user_proficiency: float,
        target_proficiency: float
    ) -> Dict[str, Any]:
        """
        Adapt project difficulty to match user's skill level
        
        Adjusts project complexity, scope, and requirements based on user's
        current proficiency vs target proficiency
        """
        logger.info(f"Adapting project difficulty for proficiency {user_proficiency} -> {target_proficiency}")
        
        # Determine current and target difficulty levels
        current_difficulty = project.get("difficulty", "intermediate")
        
        if user_proficiency < 30:
            user_level = "beginner"
        elif user_proficiency < 70:
            user_level = "intermediate"
        else:
            user_level = "advanced"
        
        if target_proficiency < 30:
            target_level = "beginner"
        elif target_proficiency < 70:
            target_level = "intermediate"
        else:
            target_level = "advanced"
        
        # If project already matches user level, return with metadata
        if current_difficulty == user_level:
            logger.info(f"Project difficulty already matches user level: {user_level}")
            adapted_project = project.copy()
            adapted_project.update({
                "adaptationNotes": f"Project difficulty already matches user level ({user_level})",
                "originalDifficulty": current_difficulty,
                "adaptedAt": datetime.utcnow().isoformat()
            })
            return adapted_project
        
        # Use AI to adapt the project
        try:
            prompt = f"""Adapt this project to match the student's skill level.

Original Project:
- Title: {project.get('title', 'Learning Project')}
- Description: {project.get('description', '')}
- Difficulty: {current_difficulty}
- Skills: {', '.join(project.get('targetSkills', []))}
- Estimated Hours: {project.get('estimatedHours', 40)}

Student Level:
- Current proficiency: {user_proficiency}%
- Target proficiency: {target_proficiency}%
- Appropriate difficulty: {user_level}

Instructions:
1. Adjust the project scope to match {user_level} level
2. Modify requirements to be appropriate for proficiency level {user_proficiency}%
3. Keep the core learning objectives but adjust complexity
4. Update estimated hours if needed

Return a JSON object with these fields:
{{
  "title": "adapted title",
  "description": "adapted description",
  "difficulty": "{user_level}",
  "targetSkills": ["skill1", "skill2"],
  "estimatedHours": number,
  "requirements": ["requirement1", "requirement2"],
  "adaptationNotes": "brief explanation of changes made"
}}"""

            response = await ai_service.call_ollama(prompt, temperature=0.7)
            
            if response:
                # Try to parse JSON response
                import json
                try:
                    # Clean response
                    response = response.strip()
                    if response.startswith("```json"):
                        response = response[7:]
                    if response.startswith("```"):
                        response = response[3:]
                    if response.endswith("```"):
                        response = response[:-3]
                    response = response.strip()
                    
                    adapted_data = json.loads(response)
                    
                    # Merge with original project
                    adapted_project = project.copy()
                    adapted_project.update({
                        "title": adapted_data.get("title", project.get("title")),
                        "description": adapted_data.get("description", project.get("description")),
                        "difficulty": adapted_data.get("difficulty", user_level),
                        "targetSkills": adapted_data.get("targetSkills", project.get("targetSkills", [])),
                        "estimatedHours": adapted_data.get("estimatedHours", project.get("estimatedHours", 40)),
                        "requirements": adapted_data.get("requirements", project.get("requirements", [])),
                        "adaptationNotes": adapted_data.get("adaptationNotes", "Adapted to match user skill level"),
                        "originalDifficulty": current_difficulty,
                        "adaptedAt": datetime.utcnow().isoformat()
                    })
                    
                    logger.info(f"Successfully adapted project from {current_difficulty} to {user_level}")
                    return adapted_project
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse AI response as JSON: {e}")
                    # Fall through to rule-based adaptation
            
        except Exception as e:
            logger.error(f"Error using AI to adapt project: {e}")
            # Fall through to rule-based adaptation
        
        # Fallback: Rule-based adaptation
        logger.info("Using rule-based adaptation")
        adapted_project = project.copy()
        
        # Adjust estimated hours based on difficulty change
        base_hours = project.get("estimatedHours", 40)
        
        difficulty_levels = ["beginner", "intermediate", "advanced"]
        current_idx = difficulty_levels.index(current_difficulty) if current_difficulty in difficulty_levels else 1
        target_idx = difficulty_levels.index(user_level)
        
        # Adjust hours: beginner = 0.7x, intermediate = 1.0x, advanced = 1.5x
        hour_multipliers = {"beginner": 0.7, "intermediate": 1.0, "advanced": 1.5}
        
        current_multiplier = hour_multipliers.get(current_difficulty, 1.0)
        target_multiplier = hour_multipliers.get(user_level, 1.0)
        
        adjusted_hours = int(base_hours * (target_multiplier / current_multiplier))
        
        # Update project
        adapted_project.update({
            "difficulty": user_level,
            "estimatedHours": adjusted_hours,
            "adaptationNotes": f"Difficulty adjusted from {current_difficulty} to {user_level} to match user proficiency level",
            "originalDifficulty": current_difficulty,
            "adaptedAt": datetime.utcnow().isoformat()
        })
        
        # Adjust description
        if user_level == "beginner" and current_difficulty != "beginner":
            adapted_project["description"] = f"[Simplified] {project.get('description', '')}"
        elif user_level == "advanced" and current_difficulty != "advanced":
            adapted_project["description"] = f"[Enhanced] {project.get('description', '')}"
        
        logger.info(f"Adapted project using rule-based approach: {current_difficulty} -> {user_level}")
        return adapted_project


# Export singleton
personalization_service = PersonalizationService()
