"""Verification service for skill verification through project completion"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4

from src.services.skill_service import skill_service
from src.services.project_service import project_service
from src.services.eligibility_service import eligibility_service
from src.utils.mock_store import mock_store
from src.models.project import ProjectStatus


class VerificationService:
    """Service for verifying skills through project completion"""
    
    @staticmethod
    async def verify_project_completion(user_id: str, project_id: str) -> Dict[str, Any]:
        """
        Mark project as complete and verify associated skills
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            Dict containing:
                - updated_skills: List of verified skills
                - skill_graph: Updated skill graph
                - eligibility_changes: Newly eligible internships
        """
        # Get project
        project = await project_service.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        
        if project.get("userId") != user_id:
            raise ValueError("Project does not belong to user")
        
        # Get target skills from project
        target_skills = project.get("targetSkills", [])
        if not target_skills:
            raise ValueError("Project has no target skills")
        
        # Get old classification for comparison
        skill_graph = await skill_service.get_skill_graph(user_id)
        internships_data = mock_store.get_all_internships()
        old_classification = eligibility_service.classify_internships_dict(skill_graph, internships_data)
        
        # Generate validation ID
        validation_id = str(uuid4())
        
        # Verify skills (set proficiency to 70, status to VERIFIED)
        skill_graph = await skill_service.verify_skills(user_id, target_skills, validation_id)
        
        # Update project status to completed
        await project_service.update_project_status(project_id, ProjectStatus.COMPLETED)
        
        # Get new classification
        skill_graph = await skill_service.get_skill_graph(user_id)
        internships_data = mock_store.get_all_internships()
        new_classification = eligibility_service.classify_internships_dict(skill_graph, internships_data)
        
        # Detect eligibility changes
        eligibility_changes = VerificationService.detect_eligibility_changes(
            old_classification,
            new_classification
        )
        
        return {
            "success": True,
            "verified_skills": target_skills,
            "skill_graph": skill_graph.dict(by_alias=True) if skill_graph else None,
            "eligibility_changes": eligibility_changes,
            "validation_id": validation_id
        }
    
    @staticmethod
    def detect_eligibility_changes(
        old_classification: Dict[str, List],
        new_classification: Dict[str, List]
    ) -> Dict[str, List]:
        """
        Detect internships that moved to better eligibility categories
        
        Args:
            old_classification: Previous classification results
            new_classification: New classification results
            
        Returns:
            Dict containing:
                - newly_eligible: Internships that became eligible
                - newly_almost_eligible: Internships that became almost eligible
        """
        # Create maps of internship IDs to categories
        old_map = {}
        for category in ["eligible", "almostEligible", "notEligible"]:
            for internship in old_classification.get(category, []):
                internship_id = internship.get("internshipId")
                if internship_id:
                    old_map[internship_id] = category
        
        new_map = {}
        for category in ["eligible", "almostEligible", "notEligible"]:
            for internship in new_classification.get(category, []):
                internship_id = internship.get("internshipId")
                if internship_id:
                    new_map[internship_id] = category
        
        # Find improvements
        newly_eligible = []
        newly_almost_eligible = []
        
        for internship_id, new_category in new_map.items():
            old_category = old_map.get(internship_id, "notEligible")
            
            # Check if moved to eligible
            if new_category == "eligible" and old_category != "eligible":
                # Find the internship details
                for internship in new_classification.get("eligible", []):
                    if internship.get("internshipId") == internship_id:
                        newly_eligible.append(internship)
                        break
            
            # Check if moved to almost eligible (but not from eligible)
            elif new_category == "almostEligible" and old_category == "notEligible":
                # Find the internship details
                for internship in new_classification.get("almostEligible", []):
                    if internship.get("internshipId") == internship_id:
                        newly_almost_eligible.append(internship)
                        break
        
        return {
            "newly_eligible": newly_eligible,
            "newly_almost_eligible": newly_almost_eligible,
            "total_improvements": len(newly_eligible) + len(newly_almost_eligible)
        }


verification_service = VerificationService()
