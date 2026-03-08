"""Explanation Service - Generate clear explanations for AI recommendations"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
from uuid import uuid4
from pydantic import BaseModel, Field
import hashlib

from src.services.ai_service import ai_service
from src.utils.mock_store import mock_store

logger = logging.getLogger(__name__)


# Data Models
class ExplanationType(str, Enum):
    """Type of explanation"""
    INTERNSHIP_MATCH = "internship_match"
    PROJECT_SUGGESTION = "project_suggestion"
    SKILL_PRIORITY = "skill_priority"
    CAREER_STEP = "career_step"


class ExplanationFactor(BaseModel):
    """Individual factor contributing to a recommendation"""
    factor_name: str = Field(alias="factorName")
    weight: float = Field(ge=0, le=1)
    value: float
    description: str
    
    class Config:
        populate_by_name = True


class Explanation(BaseModel):
    """Complete explanation for a recommendation"""
    explanation_id: str = Field(alias="explanationId")
    explanation_type: ExplanationType = Field(alias="explanationType")
    summary: str
    factors: List[ExplanationFactor]
    confidence: float = Field(ge=0, le=100)
    recommendations: List[str] = []
    created_at: str = Field(alias="createdAt")
    
    class Config:
        populate_by_name = True


class ExplanationService:
    """Service for generating clear, actionable explanations"""
    
    def _generate_cache_key(self, explanation_type: str, context: Dict[str, Any]) -> str:
        """Generate cache key for explanation"""
        # Create deterministic key from type and context
        context_str = str(sorted(context.items()))
        hash_obj = hashlib.md5(f"{explanation_type}:{context_str}".encode())
        return hash_obj.hexdigest()
    
    async def explain_internship_match(
        self,
        user_id: str,
        internship_id: str,
        match_score: float,
        matched_skills: List[str],
        missing_skills: List[Dict[str, Any]]
    ) -> Explanation:
        """
        Explain why an internship is a good/bad match
        
        Args:
            user_id: User ID
            internship_id: Internship ID
            match_score: Match score (0-100)
            matched_skills: List of matched skill names
            missing_skills: List of missing skill dictionaries
        
        Returns detailed explanation with factors
        """
        logger.info(f"Generating internship match explanation for user {user_id}, internship {internship_id}")
        
        # Check cache
        cache_key = self._generate_cache_key("internship_match", {
            "user_id": user_id,
            "internship_id": internship_id,
            "match_score": match_score
        })
        
        cached = mock_store.get_explanation(cache_key)
        if cached:
            return Explanation(**cached)
        
        # Get internship details
        internship = mock_store.get_internship(internship_id)
        if not internship:
            raise ValueError(f"Internship not found: {internship_id}")
        
        # Calculate factors
        factors = []
        
        # Factor 1: Skill Match Rate
        total_required = len(matched_skills) + len(missing_skills)
        match_rate = len(matched_skills) / total_required if total_required > 0 else 0
        
        factors.append(ExplanationFactor(
            factorName="Skill Match Rate",
            weight=0.4,
            value=match_rate * 100,
            description=f"You have {len(matched_skills)} out of {total_required} required skills"
        ))
        
        # Factor 2: Mandatory Skills Coverage
        mandatory_missing = len([s for s in missing_skills if s.get("required", False)])
        mandatory_factor = 1.0 if mandatory_missing == 0 else 0.5
        
        factors.append(ExplanationFactor(
            factorName="Mandatory Skills",
            weight=0.3,
            value=mandatory_factor * 100,
            description=f"{'All mandatory skills met' if mandatory_missing == 0 else f'{mandatory_missing} mandatory skills missing'}"
        ))
        
        # Factor 3: Proficiency Levels
        avg_gap = sum(s.get("gap", 0) for s in missing_skills) / len(missing_skills) if missing_skills else 0
        proficiency_factor = max(1.0 - (avg_gap / 100), 0)
        
        factors.append(ExplanationFactor(
            factorName="Proficiency Levels",
            weight=0.3,
            value=proficiency_factor * 100,
            description=f"Average skill gap: {int(avg_gap)} proficiency points"
        ))
        
        # Generate AI summary
        try:
            prompt = f"""Explain why this internship is a {match_score:.0f}% match for the student.

Internship: {internship.get('title', '')} at {internship.get('company', '')}
Match Score: {match_score:.1f}%

Matched Skills ({len(matched_skills)}): {', '.join(matched_skills[:5])}
Missing Skills ({len(missing_skills)}): {', '.join([s.get('skillName', '') for s in missing_skills[:5]])}

Write 2-3 sentences explaining:
1. Why this is a good/moderate/poor match
2. What the student should focus on to improve their chances
3. Realistic assessment of their readiness

Be honest but encouraging."""

            summary = await ai_service.call_ollama(prompt, temperature=0.7)
            
            if not summary or summary.startswith('{'):
                # Fallback template
                if match_score >= 80:
                    summary = f"Excellent match! You have {len(matched_skills)} of the required skills. " \
                             f"Focus on the {len(missing_skills)} remaining skills to become fully qualified."
                elif match_score >= 60:
                    summary = f"Good match with room for improvement. You meet most requirements but need to work on " \
                             f"{len(missing_skills)} skills to be fully competitive."
                else:
                    summary = f"This internship requires significant skill development. Focus on building " \
                             f"{len(missing_skills)} missing skills before applying."
        
        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            summary = f"Match score: {match_score:.1f}%. You have {len(matched_skills)} matched skills and {len(missing_skills)} skills to develop."
        
        # Create explanation
        explanation = Explanation(
            explanationId=str(uuid4()),
            explanationType=ExplanationType.INTERNSHIP_MATCH,
            summary=summary.strip(),
            factors=factors,
            confidence=match_score,
            recommendations=[
                f"Focus on learning: {', '.join([s.get('skillName', '') for s in missing_skills[:3]])}" if missing_skills else "You're ready to apply!",
                f"Estimated time to ready: {self._estimate_time_to_ready(missing_skills)}"
            ],
            createdAt=datetime.utcnow().isoformat()
        )
        
        # Cache explanation (24 hours)
        mock_store.save_explanation(cache_key, explanation.dict(by_alias=True))
        
        return explanation
    
    async def explain_project_suggestion(
        self,
        user_id: str,
        project_id: str,
        relevance_score: float,
        target_skills: List[str],
        internships_unlocked: int
    ) -> Explanation:
        """
        Explain why a project is suggested
        
        Args:
            user_id: User ID
            project_id: Project ID
            relevance_score: Relevance score (0-100)
            target_skills: Skills the project teaches
            internships_unlocked: Number of internships this project unlocks
        
        Returns detailed explanation
        """
        logger.info(f"Generating project suggestion explanation for user {user_id}, project {project_id}")
        
        # Check cache
        cache_key = self._generate_cache_key("project_suggestion", {
            "user_id": user_id,
            "project_id": project_id,
            "relevance_score": relevance_score
        })
        
        cached = mock_store.get_explanation(cache_key)
        if cached:
            return Explanation(**cached)
        
        # Get project details
        project = mock_store.get_project(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        
        # Calculate factors
        factors = []
        
        # Factor 1: Skill Gap Coverage
        factors.append(ExplanationFactor(
            factorName="Skill Gap Coverage",
            weight=0.4,
            value=relevance_score * 0.4,
            description=f"Addresses {len(target_skills)} of your priority skill gaps"
        ))
        
        # Factor 2: Career Impact
        impact_score = min(internships_unlocked * 20, 100)
        factors.append(ExplanationFactor(
            factorName="Career Impact",
            weight=0.3,
            value=impact_score,
            description=f"Could unlock {internships_unlocked} new internship opportunities"
        ))
        
        # Factor 3: Difficulty Match
        difficulty_score = relevance_score * 0.3
        factors.append(ExplanationFactor(
            factorName="Difficulty Match",
            weight=0.3,
            value=difficulty_score,
            description=f"Project difficulty matches your current skill level"
        ))
        
        # Generate AI summary
        try:
            prompt = f"""Explain why this project is recommended for the student.

Project: {project.get('title', '')}
Skills: {', '.join(target_skills)}
Relevance Score: {relevance_score:.1f}%
Impact: Unlocks {internships_unlocked} internships

Write 2-3 sentences explaining:
1. What skills they'll learn
2. How it helps their career goals
3. Why it's a good fit for their level

Be encouraging and specific."""

            summary = await ai_service.call_ollama(prompt, temperature=0.7)
            
            if not summary or summary.startswith('{'):
                # Fallback template
                summary = f"This project is highly relevant (score: {relevance_score:.1f}/100) because it teaches " \
                         f"{', '.join(target_skills[:3])} - skills you need for your target internships. " \
                         f"Completing it could unlock {internships_unlocked} new opportunities."
        
        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            summary = f"This project teaches {', '.join(target_skills)} and could unlock {internships_unlocked} internships."
        
        # Create explanation
        explanation = Explanation(
            explanationId=str(uuid4()),
            explanationType=ExplanationType.PROJECT_SUGGESTION,
            summary=summary.strip(),
            factors=factors,
            confidence=relevance_score,
            recommendations=[
                f"Start with: {target_skills[0]}" if target_skills else "Begin the project",
                f"Estimated completion: {project.get('estimatedHours', 40)} hours"
            ],
            createdAt=datetime.utcnow().isoformat()
        )
        
        # Cache explanation
        mock_store.save_explanation(cache_key, explanation.dict(by_alias=True))
        
        return explanation
    
    async def explain_skill_priority(
        self,
        user_id: str,
        skill_name: str,
        priority_score: float,
        internships_impacted: int,
        gap_size: int
    ) -> Explanation:
        """
        Explain why a skill is high/low priority
        
        Args:
            user_id: User ID
            skill_name: Skill name
            priority_score: Priority score (0-100)
            internships_impacted: Number of internships requiring this skill
            gap_size: Proficiency gap size
        
        Returns detailed explanation
        """
        logger.info(f"Generating skill priority explanation for {skill_name}")
        
        # Check cache
        cache_key = self._generate_cache_key("skill_priority", {
            "user_id": user_id,
            "skill_name": skill_name,
            "priority_score": priority_score
        })
        
        cached = mock_store.get_explanation(cache_key)
        if cached:
            return Explanation(**cached)
        
        # Calculate factors
        factors = []
        
        # Factor 1: Gap Urgency
        gap_urgency = min(gap_size * 1.2, 100)
        factors.append(ExplanationFactor(
            factorName="Gap Urgency",
            weight=0.4,
            value=gap_urgency,
            description=f"You need {gap_size} proficiency points to meet requirements"
        ))
        
        # Factor 2: Market Demand
        demand_score = min(internships_impacted * 10, 100)
        factors.append(ExplanationFactor(
            factorName="Market Demand",
            weight=0.3,
            value=demand_score,
            description=f"Required by {internships_impacted} internships in your targets"
        ))
        
        # Factor 3: Career Impact
        impact_score = priority_score * 0.3
        factors.append(ExplanationFactor(
            factorName="Career Impact",
            weight=0.3,
            value=impact_score,
            description=f"High impact on your career progression"
        ))
        
        # Generate AI summary
        try:
            prompt = f"""Explain why {skill_name} is a priority skill for this student.

Priority Score: {priority_score:.1f}/100
Gap Size: {gap_size} proficiency points
Internships Requiring This: {internships_impacted}

Write 2-3 sentences explaining:
1. Why this skill is important for their career
2. How learning it will help them
3. What opportunities it unlocks

Be specific and motivating."""

            summary = await ai_service.call_ollama(prompt, temperature=0.7)
            
            if not summary or summary.startswith('{'):
                # Fallback template
                if priority_score >= 70:
                    summary = f"{skill_name} is a high-priority skill because it's required by {internships_impacted} of your target internships. " \
                             f"Closing this {gap_size}-point gap will significantly improve your eligibility."
                else:
                    summary = f"{skill_name} is moderately important for your career goals. " \
                             f"It's required by {internships_impacted} internships and has a {gap_size}-point gap."
        
        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            summary = f"{skill_name} priority: {priority_score:.1f}/100. Required by {internships_impacted} internships."
        
        # Create explanation
        explanation = Explanation(
            explanationId=str(uuid4()),
            explanationType=ExplanationType.SKILL_PRIORITY,
            summary=summary.strip(),
            factors=factors,
            confidence=priority_score,
            recommendations=[
                f"Estimated learning time: {gap_size * 1.5:.0f} hours",
                f"Will unlock {internships_impacted} internship opportunities"
            ],
            createdAt=datetime.utcnow().isoformat()
        )
        
        # Cache explanation
        mock_store.save_explanation(cache_key, explanation.dict(by_alias=True))
        
        return explanation
    
    async def explain_career_step(
        self,
        user_id: str,
        milestone_title: str,
        milestone_description: str,
        skills_to_acquire: List[str],
        estimated_weeks: int
    ) -> Explanation:
        """
        Explain why a career milestone is recommended
        
        Args:
            user_id: User ID
            milestone_title: Milestone title
            milestone_description: Milestone description
            skills_to_acquire: Skills in this milestone
            estimated_weeks: Estimated duration
        
        Returns detailed explanation
        """
        logger.info(f"Generating career step explanation for milestone: {milestone_title}")
        
        # Check cache
        cache_key = self._generate_cache_key("career_step", {
            "user_id": user_id,
            "milestone_title": milestone_title
        })
        
        cached = mock_store.get_explanation(cache_key)
        if cached:
            return Explanation(**cached)
        
        # Calculate factors
        factors = []
        
        # Factor 1: Skill Development
        factors.append(ExplanationFactor(
            factorName="Skill Development",
            weight=0.4,
            value=len(skills_to_acquire) * 20,
            description=f"Develops {len(skills_to_acquire)} essential skills"
        ))
        
        # Factor 2: Timeline Feasibility
        feasibility_score = 100 if estimated_weeks <= 8 else 70 if estimated_weeks <= 16 else 50
        factors.append(ExplanationFactor(
            factorName="Timeline Feasibility",
            weight=0.3,
            value=feasibility_score,
            description=f"Achievable in {estimated_weeks} weeks with consistent effort"
        ))
        
        # Factor 3: Career Progression
        factors.append(ExplanationFactor(
            factorName="Career Progression",
            weight=0.3,
            value=80,
            description="Critical step in your career roadmap"
        ))
        
        # Generate AI summary
        try:
            prompt = f"""Explain why this career milestone is important for the student.

Milestone: {milestone_title}
Description: {milestone_description}
Skills to Learn: {', '.join(skills_to_acquire)}
Duration: {estimated_weeks} weeks

Write 2-3 sentences explaining:
1. Why this milestone matters for their career
2. What they'll achieve by completing it
3. How it prepares them for the next step

Be motivating and clear."""

            summary = await ai_service.call_ollama(prompt, temperature=0.7)
            
            if not summary or summary.startswith('{'):
                # Fallback template
                summary = f"This milestone is essential for your career progression. " \
                         f"By mastering {', '.join(skills_to_acquire[:3])}, you'll build the foundation " \
                         f"needed for the next phase of your journey."
        
        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            summary = f"{milestone_title}: Learn {', '.join(skills_to_acquire[:3])} in {estimated_weeks} weeks."
        
        # Create explanation
        explanation = Explanation(
            explanationId=str(uuid4()),
            explanationType=ExplanationType.CAREER_STEP,
            summary=summary.strip(),
            factors=factors,
            confidence=80.0,
            recommendations=[
                f"Focus on: {skills_to_acquire[0]}" if skills_to_acquire else "Start learning",
                f"Complete in: {estimated_weeks} weeks"
            ],
            createdAt=datetime.utcnow().isoformat()
        )
        
        # Cache explanation
        mock_store.save_explanation(cache_key, explanation.dict(by_alias=True))
        
        return explanation
    
    async def generate_batch_explanations(
        self,
        explanations_requests: List[Dict[str, Any]]
    ) -> List[Explanation]:
        """
        Generate multiple explanations in batch
        
        Args:
            explanations_requests: List of explanation request dictionaries
        
        Returns list of explanations
        """
        logger.info(f"Generating {len(explanations_requests)} explanations in batch")
        
        explanations = []
        
        for request in explanations_requests:
            try:
                exp_type = request.get("type")
                
                if exp_type == "internship_match":
                    explanation = await self.explain_internship_match(
                        user_id=request["userId"],
                        internship_id=request["internshipId"],
                        match_score=request["matchScore"],
                        matched_skills=request.get("matchedSkills", []),
                        missing_skills=request.get("missingSkills", [])
                    )
                    explanations.append(explanation)
                
                elif exp_type == "project_suggestion":
                    explanation = await self.explain_project_suggestion(
                        user_id=request["userId"],
                        project_id=request["projectId"],
                        relevance_score=request["relevanceScore"],
                        target_skills=request.get("targetSkills", []),
                        internships_unlocked=request.get("internshipsUnlocked", 0)
                    )
                    explanations.append(explanation)
                
                elif exp_type == "skill_priority":
                    explanation = await self.explain_skill_priority(
                        user_id=request["userId"],
                        skill_name=request["skillName"],
                        priority_score=request["priorityScore"],
                        internships_impacted=request.get("internshipsImpacted", 0),
                        gap_size=request.get("gapSize", 0)
                    )
                    explanations.append(explanation)
                
                elif exp_type == "career_step":
                    explanation = await self.explain_career_step(
                        user_id=request["userId"],
                        milestone_title=request["milestoneTitle"],
                        milestone_description=request.get("milestoneDescription", ""),
                        skills_to_acquire=request.get("skillsToAcquire", []),
                        estimated_weeks=request.get("estimatedWeeks", 4)
                    )
                    explanations.append(explanation)
                
                else:
                    logger.warning(f"Unknown explanation type: {exp_type}")
            
            except Exception as e:
                logger.error(f"Error generating explanation: {e}")
                continue
        
        logger.info(f"Generated {len(explanations)} explanations")
        return explanations
    
    def _estimate_time_to_ready(self, missing_skills: List[Dict[str, Any]]) -> str:
        """Estimate time needed to acquire missing skills"""
        if not missing_skills:
            return "Ready now"
        
        total_gap = sum(s.get("gap", 0) for s in missing_skills)
        hours = total_gap * 1.5
        
        if hours < 40:
            return "1-2 weeks"
        elif hours < 80:
            return "3-4 weeks"
        elif hours < 160:
            return "2-3 months"
        else:
            return "3-6 months"


# Export singleton
explanation_service = ExplanationService()
