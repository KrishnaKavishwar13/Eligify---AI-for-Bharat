"""Skill graph service - Mock mode for local development"""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from src.config.settings import settings
from src.models.skill import SkillGraph, SkillNode, SkillStatus, SkillCategory, SkillSource
from src.utils.validation import normalize_skill_name
from src.utils.mock_store import mock_store


class SkillService:
    """Service for managing student skill graphs"""
    
    @staticmethod
    async def initialize_skill_graph(user_id: str, initial_skills: List[dict]) -> SkillGraph:
        """Initialize skill graph for new user"""
        now = datetime.utcnow().isoformat()
        
        skills = []
        for skill_data in initial_skills:
            skill = SkillNode(
                skillId=str(uuid4()),
                name=skill_data["name"],
                normalizedName=normalize_skill_name(skill_data["name"]),
                category=SkillCategory(skill_data.get("category", "tool")),
                status=SkillStatus.CLAIMED,
                proficiencyLevel=skill_data.get("proficiency", 0),
                verified=False,
                source=SkillSource.RESUME,
                relatedSkills=[],
                prerequisites=[],
                addedAt=now,
                lastUpdatedAt=now
            )
            skills.append(skill)
        
        skill_graph = SkillGraph(
            userId=user_id,
            skills=skills,
            totalSkills=len(skills),
            verifiedSkills=0,
            inProgressSkills=0,
            lastUpdated=now
        )
        
        mock_store.save_skill_graph(user_id, skill_graph.dict(by_alias=True))
        return skill_graph
    
    @staticmethod
    async def get_skill_graph(user_id: str) -> Optional[SkillGraph]:
        """Get user's skill graph from mock store"""
        item = mock_store.get_skill_graph(user_id)
        if not item:
            return None
        
        # Convert camelCase keys to snake_case for Pydantic model
        # The mock store saves in camelCase, but SkillGraph expects snake_case
        try:
            return SkillGraph(**item)
        except Exception as e:
            # If validation fails, try to return the raw dict
            print(f"Error creating SkillGraph: {e}")
            print(f"Item data: {item}")
            return None
    
    @staticmethod
    async def add_skill(user_id: str, skill_name: str, category: str, proficiency: int = 0) -> SkillNode:
        """Add new skill to graph"""
        now = datetime.utcnow().isoformat()
        
        skill = SkillNode(
            skillId=str(uuid4()),
            name=skill_name,
            normalizedName=normalize_skill_name(skill_name),
            category=SkillCategory(category),
            status=SkillStatus.CLAIMED,
            proficiencyLevel=proficiency,
            verified=False,
            source=SkillSource.MANUAL,
            relatedSkills=[],
            prerequisites=[],
            addedAt=now,
            lastUpdatedAt=now
        )
        
        # Get current graph
        graph = await SkillService.get_skill_graph(user_id)
        if graph:
            graph.skills.append(skill)
            graph.total_skills += 1
            graph.last_updated = now
            mock_store.save_skill_graph(user_id, graph.dict(by_alias=True))
        
        return skill
    
    @staticmethod
    async def verify_skills(user_id: str, skill_names: List[str], validation_id: str) -> SkillGraph:
        """Mark skills as verified"""
        now = datetime.utcnow().isoformat()
        
        graph = await SkillService.get_skill_graph(user_id)
        if not graph:
            return None
        
        verified_count = 0
        for skill in graph.skills:
            if skill.name in skill_names:
                skill.status = SkillStatus.VERIFIED
                skill.verified = True
                skill.verified_at = now
                skill.validation_id = validation_id
                skill.proficiency_level = max(skill.proficiency_level, 70)
                skill.last_updated_at = now
                verified_count += 1
        
        graph.verified_skills = sum(1 for s in graph.skills if s.verified)
        graph.last_updated = now
        
        mock_store.save_skill_graph(user_id, graph.dict(by_alias=True))
        return graph
    
    @staticmethod
    async def update_skill_status(user_id: str, skill_id: str, status: SkillStatus) -> SkillNode:
        """Update skill status"""
        now = datetime.utcnow().isoformat()
        
        graph = await SkillService.get_skill_graph(user_id)
        if not graph:
            return None
        
        for skill in graph.skills:
            if skill.skill_id == skill_id:
                skill.status = status
                skill.last_updated_at = now
                
                # Update verified flag if status is VERIFIED
                if status == SkillStatus.VERIFIED:
                    skill.verified = True
                    skill.verified_at = now
                    skill.proficiency_level = max(skill.proficiency_level, 70)
                
                break
        
        # Recalculate counts
        graph.verified_skills = sum(1 for s in graph.skills if s.verified)
        graph.in_progress_skills = sum(1 for s in graph.skills if s.status == SkillStatus.IN_PROGRESS)
        graph.last_updated = now
        
        mock_store.save_skill_graph(user_id, graph.dict(by_alias=True))
        return skill
    
    @staticmethod
    async def get_skill_gaps(user_id: str, required_skills: List[dict]) -> List[dict]:
        """Calculate skill gaps for required skills"""
        graph = await SkillService.get_skill_graph(user_id)
        if not graph:
            return []
        
        # Create a map of user skills
        user_skills_map = {skill.normalizedName: skill for skill in graph.skills}
        
        gaps = []
        for req_skill in required_skills:
            skill_name = req_skill.get("name", "")
            normalized_name = normalize_skill_name(skill_name)
            required_proficiency = req_skill.get("proficiencyLevel", 50)
            mandatory = req_skill.get("mandatory", False)
            
            user_skill = user_skills_map.get(normalized_name)
            
            if not user_skill:
                # Skill missing entirely
                gaps.append({
                    "skillName": skill_name,
                    "required": mandatory,
                    "currentProficiency": 0,
                    "targetProficiency": required_proficiency,
                    "priority": "high" if mandatory else "medium"
                })
            elif user_skill.proficiencyLevel < required_proficiency:
                # Skill exists but proficiency too low
                gaps.append({
                    "skillName": skill_name,
                    "required": mandatory,
                    "currentProficiency": user_skill.proficiencyLevel,
                    "targetProficiency": required_proficiency,
                    "priority": "high" if mandatory else "low"
                })
        
        return gaps


skill_service = SkillService()
