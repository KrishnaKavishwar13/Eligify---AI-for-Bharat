"""Deterministic eligibility engine - NO AI"""

from typing import List, Dict, Any
from src.models.skill import SkillGraph
from src.models.internship import Internship, InternshipMatch, ClassifiedInternships, RequiredSkill
from src.utils.validation import normalize_skill_name


class EligibilityService:
    """Deterministic eligibility classification engine"""
    
    @staticmethod
    def calculate_match_score(
        user_skills: SkillGraph,
        internship: Internship
    ) -> InternshipMatch:
        """
        Calculate match score between user skills and internship requirements
        Pure deterministic algorithm - NO AI
        """
        total_weight = 0.0
        achieved_weight = 0.0
        matched_skills = []
        missing_skills = []
        missing_mandatory_count = 0
        
        # Create skill lookup map
        skill_map = {
            normalize_skill_name(skill.name): skill
            for skill in user_skills.skills
        }
        
        # Evaluate each required skill
        for req_skill in internship.required_skills:
            total_weight += req_skill.weight
            normalized_req = normalize_skill_name(req_skill.name)
            
            user_skill = skill_map.get(normalized_req)
            
            if user_skill:
                # Calculate proficiency gap
                proficiency_gap = req_skill.proficiency_level - user_skill.proficiency_level
                
                if proficiency_gap <= 0:
                    # Student meets or exceeds requirement
                    achieved_weight += req_skill.weight
                    matched_skills.append(req_skill.name)
                elif proficiency_gap <= 20:
                    # Close enough - partial credit
                    partial_credit = req_skill.weight * (1 - proficiency_gap / 100)
                    achieved_weight += partial_credit
                    matched_skills.append(req_skill.name)
                else:
                    # Significant gap
                    missing_skills.append({
                        "skillName": req_skill.name,
                        "required": req_skill.mandatory,
                        "currentProficiency": user_skill.proficiency_level,
                        "targetProficiency": req_skill.proficiency_level,
                        "priority": "high" if req_skill.mandatory else "medium"
                    })
                    if req_skill.mandatory:
                        missing_mandatory_count += 1
            else:
                # Skill not found
                missing_skills.append({
                    "skillName": req_skill.name,
                    "required": req_skill.mandatory,
                    "currentProficiency": 0,
                    "targetProficiency": req_skill.proficiency_level,
                    "priority": "high" if req_skill.mandatory else "medium"
                })
                if req_skill.mandatory:
                    missing_mandatory_count += 1
        
        # Calculate final match score
        match_score = (achieved_weight / total_weight * 100) if total_weight > 0 else 0
        
        return InternshipMatch(
            internship=internship,
            matchScore=round(match_score, 2),
            missingSkills=missing_skills,
            matchedSkills=matched_skills,
            missingMandatorySkills=missing_mandatory_count
        )
    
    @staticmethod
    def classify_internships(
        user_skills: SkillGraph,
        internships: List[Internship]
    ) -> ClassifiedInternships:
        """
        Classify internships into eligibility categories
        Pure deterministic algorithm - NO AI
        """
        eligible = []
        almost_eligible = []
        not_eligible = []
        
        for internship in internships:
            match_result = EligibilityService.calculate_match_score(user_skills, internship)
            
            # Classification thresholds
            if match_result.matchScore >= 80 and match_result.missingMandatorySkills == 0:
                eligible.append(match_result)
            elif match_result.matchScore >= 50 and match_result.missingMandatorySkills <= 2:
                almost_eligible.append(match_result)
            else:
                not_eligible.append(match_result)
        
        # Sort by match score descending
        eligible.sort(key=lambda x: x.matchScore, reverse=True)
        almost_eligible.sort(key=lambda x: x.matchScore, reverse=True)
        not_eligible.sort(key=lambda x: x.matchScore, reverse=True)
        
        return ClassifiedInternships(
            eligible=eligible,
            almostEligible=almost_eligible,
            notEligible=not_eligible
        )
    
    @staticmethod
    def classify_internships_dict(
        user_skills: SkillGraph,
        internships_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Classify internships using dict data (no Pydantic models)
        Pure deterministic algorithm - NO AI
        """
        eligible = []
        almost_eligible = []
        not_eligible = []
        
        # Create skill lookup map
        skill_map = {
            normalize_skill_name(skill.name): skill
            for skill in user_skills.skills
        }
        
        for internship_data in internships_data:
            total_weight = 0.0
            achieved_weight = 0.0
            matched_skills = []
            missing_skills = []
            missing_mandatory_count = 0
            
            # Evaluate each required skill
            for req_skill in internship_data.get("requiredSkills", []):
                weight = req_skill.get("weight", 1.0)
                total_weight += weight
                normalized_req = normalize_skill_name(req_skill["name"])
                
                user_skill = skill_map.get(normalized_req)
                
                if user_skill:
                    # Calculate proficiency gap
                    proficiency_gap = req_skill["proficiencyLevel"] - user_skill.proficiency_level
                    
                    if proficiency_gap <= 0:
                        # Student meets or exceeds requirement
                        achieved_weight += weight
                        matched_skills.append(req_skill["name"])
                    elif proficiency_gap <= 20:
                        # Close enough - partial credit
                        partial_credit = weight * (1 - proficiency_gap / 100)
                        achieved_weight += partial_credit
                        matched_skills.append(req_skill["name"])
                    else:
                        # Significant gap
                        missing_skills.append({
                            "skillName": req_skill["name"],
                            "required": req_skill.get("mandatory", False),
                            "currentProficiency": user_skill.proficiency_level,
                            "targetProficiency": req_skill["proficiencyLevel"],
                            "priority": "high" if req_skill.get("mandatory", False) else "medium",
                            "gap": proficiency_gap
                        })
                        if req_skill.get("mandatory", False):
                            missing_mandatory_count += 1
                else:
                    # Skill not found
                    missing_skills.append({
                        "skillName": req_skill["name"],
                        "required": req_skill.get("mandatory", False),
                        "currentProficiency": 0,
                        "targetProficiency": req_skill["proficiencyLevel"],
                        "priority": "high" if req_skill.get("mandatory", False) else "medium",
                        "gap": req_skill["proficiencyLevel"]
                    })
                    if req_skill.get("mandatory", False):
                        missing_mandatory_count += 1
            
            # Calculate final match score
            match_score = round((achieved_weight / total_weight * 100), 2) if total_weight > 0 else 0
            
            # Create result dict with internship wrapped
            result = {
                "internship": internship_data,
                "matchScore": match_score,
                "missingSkills": missing_skills,
                "matchedSkills": matched_skills
            }
            
            # Classification thresholds
            if match_score >= 80 and missing_mandatory_count == 0:
                eligible.append(result)
            elif match_score >= 50 and missing_mandatory_count <= 2:
                almost_eligible.append(result)
            else:
                not_eligible.append(result)
        
        # Sort by match score descending
        eligible.sort(key=lambda x: x["matchScore"], reverse=True)
        almost_eligible.sort(key=lambda x: x["matchScore"], reverse=True)
        not_eligible.sort(key=lambda x: x["matchScore"], reverse=True)
        
        return {
            "eligible": eligible,
            "almostEligible": almost_eligible,
            "notEligible": not_eligible
        }


eligibility_service = EligibilityService()
