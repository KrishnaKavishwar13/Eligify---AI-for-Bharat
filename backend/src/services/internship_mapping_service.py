"""Internship Mapping Service - Creates skill-internship relationship graphs"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Set, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

from src.utils.validation import normalize_skill_name
from src.utils.mock_store import mock_store

logger = logging.getLogger(__name__)


# Data Models
class SkillInternshipMapping(BaseModel):
    """Mapping between skill and internships"""
    skill_name: str = Field(alias="skillName")
    normalized_name: str = Field(alias="normalizedName")
    category: str
    internship_ids: List[str] = Field(alias="internshipIds")
    average_proficiency_required: int = Field(alias="averageProficiencyRequired", ge=0, le=100)
    min_proficiency_required: int = Field(alias="minProficiencyRequired", ge=0, le=100)
    max_proficiency_required: int = Field(alias="maxProficiencyRequired", ge=0, le=100)
    mandatory_count: int = Field(alias="mandatoryCount")
    total_count: int = Field(alias="totalCount")
    weight_sum: float = Field(alias="weightSum")

    class Config:
        populate_by_name = True


class InternshipCluster(BaseModel):
    """Cluster of related internships"""
    cluster_id: str = Field(alias="clusterId")
    cluster_name: str = Field(alias="clusterName")
    internship_ids: List[str] = Field(alias="internshipIds")
    common_skills: List[str] = Field(alias="commonSkills")
    skill_overlap_score: float = Field(alias="skillOverlapScore")

    class Config:
        populate_by_name = True


class SkillDependency(BaseModel):
    """Skill dependency relationship"""
    skill_name: str = Field(alias="skillName")
    prerequisites: List[str]
    related_skills: List[str] = Field(alias="relatedSkills")
    dependent_skills: List[str] = Field(alias="dependentSkills")
    learning_order: int = Field(alias="learningOrder")

    class Config:
        populate_by_name = True


class InternshipSkillGraph(BaseModel):
    """Complete graph of internship-skill relationships"""
    graph_id: str = Field(alias="graphId")
    skill_mappings: Dict[str, SkillInternshipMapping] = Field(alias="skillMappings")
    internship_clusters: List[InternshipCluster] = Field(alias="internshipClusters")
    skill_dependencies: Dict[str, SkillDependency] = Field(alias="skillDependencies")
    total_internships: int = Field(alias="totalInternships")
    total_unique_skills: int = Field(alias="totalUniqueSkills")
    last_updated: str = Field(alias="lastUpdated")

    class Config:
        populate_by_name = True


class InternshipMappingService:
    """Service for creating and maintaining skill-internship relationship graphs"""
    
    async def build_skill_internship_graph(
        self,
        internships: Optional[List[Dict[str, Any]]] = None
    ) -> InternshipSkillGraph:
        """
        Build complete mapping of skills to internships
        
        Returns graph with skill mappings, clusters, and dependencies
        """
        logger.info("Building skill-internship graph")
        
        # Get all internships if not provided
        if internships is None:
            internships = mock_store.get_all_internships()
        
        if not internships:
            logger.warning("No internships available for graph building")
            return InternshipSkillGraph(
                graphId=str(uuid4()),
                skillMappings={},
                internshipClusters=[],
                skillDependencies={},
                totalInternships=0,
                totalUniqueSkills=0,
                lastUpdated=datetime.utcnow().isoformat()
            )
        
        # Step 1: Build skill mappings
        skill_mappings = {}
        
        for internship in internships:
            internship_id = internship.get("internshipId")
            
            for req_skill in internship.get("requiredSkills", []):
                skill_name = req_skill["name"]
                skill_key = normalize_skill_name(skill_name)
                proficiency = req_skill["proficiencyLevel"]
                mandatory = req_skill.get("mandatory", False)
                weight = req_skill.get("weight", 1.0)
                category = req_skill.get("category", "tool")
                
                if skill_key not in skill_mappings:
                    skill_mappings[skill_key] = {
                        "skillName": skill_name,
                        "normalizedName": skill_key,
                        "category": category,
                        "internshipIds": [internship_id],
                        "proficiencies": [proficiency],
                        "mandatoryCount": 1 if mandatory else 0,
                        "totalCount": 1,
                        "weightSum": weight
                    }
                else:
                    skill_mappings[skill_key]["internshipIds"].append(internship_id)
                    skill_mappings[skill_key]["proficiencies"].append(proficiency)
                    skill_mappings[skill_key]["mandatoryCount"] += (1 if mandatory else 0)
                    skill_mappings[skill_key]["totalCount"] += 1
                    skill_mappings[skill_key]["weightSum"] += weight
        
        # Calculate proficiency statistics
        final_mappings = {}
        for skill_key, data in skill_mappings.items():
            profs = data["proficiencies"]
            final_mappings[skill_key] = SkillInternshipMapping(
                skillName=data["skillName"],
                normalizedName=data["normalizedName"],
                category=data["category"],
                internshipIds=data["internshipIds"],
                averageProficiencyRequired=int(sum(profs) / len(profs)),
                minProficiencyRequired=min(profs),
                maxProficiencyRequired=max(profs),
                mandatoryCount=data["mandatoryCount"],
                totalCount=data["totalCount"],
                weightSum=data["weightSum"]
            )
        
        # Step 2: Find skill clusters
        clusters = self.find_skill_clusters(internships)
        
        # Step 3: Build skill dependencies (simplified - no AI for now)
        dependencies = self.build_skill_dependencies(final_mappings)
        
        # Step 4: Create graph
        graph = InternshipSkillGraph(
            graphId=str(uuid4()),
            skillMappings=final_mappings,
            internshipClusters=clusters,
            skillDependencies=dependencies,
            totalInternships=len(internships),
            totalUniqueSkills=len(final_mappings),
            lastUpdated=datetime.utcnow().isoformat()
        )
        
        # Cache the graph
        mock_store.save_internship_skill_graph(graph.dict(by_alias=True))
        
        logger.info(f"Graph built: {len(final_mappings)} skills, {len(clusters)} clusters")
        return graph
    
    def find_skill_clusters(self, internships: List[Dict[str, Any]]) -> List[InternshipCluster]:
        """Find clusters of internships with similar skill requirements"""
        clusters = []
        
        # Simple clustering: group by common skills
        # For MVP, create clusters based on primary skill category
        category_groups = {}
        
        for internship in internships:
            internship_id = internship.get("internshipId")
            skills = [req["name"] for req in internship.get("requiredSkills", [])]
            
            # Determine primary category (most common)
            categories = [req.get("category", "tool") for req in internship.get("requiredSkills", [])]
            if categories:
                primary_category = max(set(categories), key=categories.count)
                
                if primary_category not in category_groups:
                    category_groups[primary_category] = {
                        "internships": [],
                        "all_skills": set()
                    }
                
                category_groups[primary_category]["internships"].append(internship_id)
                category_groups[primary_category]["all_skills"].update(skills)
        
        # Create clusters
        for category, data in category_groups.items():
            if len(data["internships"]) >= 2:  # At least 2 internships
                cluster = InternshipCluster(
                    clusterId=str(uuid4()),
                    clusterName=f"{category.replace('_', ' ').title()} Roles",
                    internshipIds=data["internships"],
                    commonSkills=list(data["all_skills"])[:10],  # Top 10
                    skillOverlapScore=len(data["all_skills"]) / len(data["internships"])
                )
                clusters.append(cluster)
        
        return clusters
    
    def build_skill_dependencies(
        self,
        skill_mappings: Dict[str, SkillInternshipMapping]
    ) -> Dict[str, SkillDependency]:
        """Build skill dependency relationships (simplified)"""
        dependencies = {}
        
        # Hardcoded common dependencies for MVP
        common_deps = {
            "react": ["javascript", "html", "css"],
            "nodejs": ["javascript"],
            "express": ["nodejs", "javascript"],
            "mongodb": ["database"],
            "postgresql": ["sql", "database"],
            "django": ["python"],
            "flask": ["python"],
            "fastapi": ["python"],
            "docker": ["linux"],
            "kubernetes": ["docker", "linux"],
            "aws": ["cloud"],
            "typescript": ["javascript"]
        }
        
        for skill_key, mapping in skill_mappings.items():
            prereqs = []
            related = []
            
            # Check if skill has known prerequisites
            if skill_key in common_deps:
                prereqs = [p for p in common_deps[skill_key] if p in skill_mappings]
            
            # Find related skills (same category, similar usage)
            for other_key, other_mapping in skill_mappings.items():
                if other_key != skill_key and other_mapping.category == mapping.category:
                    # Check if used in similar internships
                    overlap = set(mapping.internship_ids) & set(other_mapping.internship_ids)
                    if len(overlap) >= 2:  # At least 2 common internships
                        related.append(other_mapping.skill_name)
            
            dependencies[skill_key] = SkillDependency(
                skillName=mapping.skill_name,
                prerequisites=prereqs,
                relatedSkills=related[:5],  # Top 5
                dependentSkills=[],  # Will be populated in reverse pass
                learningOrder=0  # Will be calculated
            )
        
        return dependencies
    
    async def get_internships_by_skill(
        self,
        skill_name: str,
        min_proficiency: int = 0
    ) -> List[str]:
        """Get internships requiring specific skill"""
        # Get cached graph
        graph_data = mock_store.get_internship_skill_graph()
        
        if not graph_data:
            # Build graph if not cached
            graph = await self.build_skill_internship_graph()
            graph_data = graph.dict(by_alias=True)
        
        skill_key = normalize_skill_name(skill_name)
        skill_mappings = graph_data.get("skillMappings", {})
        
        if skill_key not in skill_mappings:
            return []
        
        mapping = skill_mappings[skill_key]
        
        # Filter by minimum proficiency if specified
        if min_proficiency > 0:
            # Would need to check each internship - simplified for MVP
            return mapping["internshipIds"]
        
        return mapping["internshipIds"]
    
    async def get_skill_dependencies(self, skill_name: str) -> Dict[str, Any]:
        """Get prerequisite and related skills"""
        # Get cached graph
        graph_data = mock_store.get_internship_skill_graph()
        
        if not graph_data:
            graph = await self.build_skill_internship_graph()
            graph_data = graph.dict(by_alias=True)
        
        skill_key = normalize_skill_name(skill_name)
        dependencies = graph_data.get("skillDependencies", {})
        
        if skill_key not in dependencies:
            return {
                "prerequisites": [],
                "relatedSkills": [],
                "dependentSkills": []
            }
        
        dep = dependencies[skill_key]
        return {
            "prerequisites": dep.get("prerequisites", []),
            "relatedSkills": dep.get("relatedSkills", []),
            "dependentSkills": dep.get("dependentSkills", [])
        }
    
    async def calculate_skill_impact(
        self,
        skill_name: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Calculate how learning a skill impacts eligibility"""
        from src.services.skill_service import skill_service
        from src.services.eligibility_service import eligibility_service
        
        # Get current skill graph
        skill_graph = await skill_service.get_skill_graph(user_id)
        if not skill_graph:
            return {
                "currentEligible": 0,
                "projectedEligible": 0,
                "newOpportunities": 0,
                "impactScore": 0.0
            }
        
        # Get all internships
        all_internships = mock_store.get_all_internships()
        
        # Calculate current eligibility
        current_classification = eligibility_service.classify_internships_dict(
            skill_graph,
            all_internships
        )
        current_eligible = len(current_classification["eligible"])
        
        # Simulate adding the skill at 70% proficiency
        simulated_skills = skill_graph.skills.copy()
        from src.models.skill import SkillNode, SkillStatus, SkillCategory, SkillSource
        
        # Check if skill already exists
        skill_exists = any(
            normalize_skill_name(s.name) == normalize_skill_name(skill_name)
            for s in simulated_skills
        )
        
        if not skill_exists:
            new_skill = SkillNode(
                skillId=str(uuid4()),
                name=skill_name,
                normalizedName=normalize_skill_name(skill_name),
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
        from src.models.skill import SkillGraph
        simulated_graph = SkillGraph(
            userId=user_id,
            skills=simulated_skills,
            totalSkills=len(simulated_skills),
            verifiedSkills=skill_graph.verified_skills + (0 if skill_exists else 1),
            inProgressSkills=skill_graph.in_progress_skills,
            lastUpdated=datetime.utcnow().isoformat()
        )
        
        # Calculate projected eligibility
        projected_classification = eligibility_service.classify_internships_dict(
            simulated_graph,
            all_internships
        )
        projected_eligible = len(projected_classification["eligible"])
        
        # Calculate impact
        new_opportunities = projected_eligible - current_eligible
        impact_score = (new_opportunities / len(all_internships) * 100) if all_internships else 0.0
        
        return {
            "currentEligible": current_eligible,
            "projectedEligible": projected_eligible,
            "newOpportunities": new_opportunities,
            "impactScore": round(impact_score, 2)
        }


# Export singleton
internship_mapping_service = InternshipMappingService()
