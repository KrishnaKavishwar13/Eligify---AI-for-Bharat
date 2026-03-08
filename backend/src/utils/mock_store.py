"""Mock data store for local development without AWS services"""

from typing import Dict, Any, Optional
import json
from pathlib import Path

# Import enhanced store
from src.utils.enhanced_store import enhanced_store

# Legacy in-memory storage (kept for backward compatibility)
MOCK_USERS: Dict[str, Any] = {}
MOCK_PROFILES: Dict[str, Any] = {}
MOCK_SKILLS: Dict[str, Any] = {}
MOCK_INTERNSHIPS: Dict[str, Any] = {}
MOCK_PROJECTS: Dict[str, Any] = {}
MOCK_SKILL_GAP_ANALYSES: Dict[str, Any] = {}
MOCK_INTERNSHIP_SKILL_GRAPH: Optional[Dict[str, Any]] = None
MOCK_PERSONALIZED_SUGGESTIONS: Dict[str, Any] = {}
MOCK_CAREER_ROADMAPS: Dict[str, Any] = {}
MOCK_EXPLANATION_CACHE: Dict[str, Any] = {}


def load_internships_from_file() -> Dict[str, Any]:
    """Load internships from seed data file"""
    data_file = Path(__file__).parent.parent.parent / "data" / "internships.json"
    
    if data_file.exists():
        with open(data_file, "r") as f:
            internships_list = json.load(f)
            # Convert list to dict with internshipId as key (camelCase format)
            return {i["internshipId"]: i for i in internships_list}
    
    return {}


# Initialize internships from seed data
MOCK_INTERNSHIPS = load_internships_from_file()


class MockStore:
    """Mock data store - now powered by EnhancedStore for persistence and performance"""
    
    @staticmethod
    def get_user(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return enhanced_store.get_user(user_id)
    
    @staticmethod
    def save_user(user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save user data"""
        return enhanced_store.save_user(user_id, user_data)
    
    @staticmethod
    def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
        """Get profile by user ID"""
        return enhanced_store.get_profile(user_id)
    
    @staticmethod
    def save_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save profile data"""
        return enhanced_store.save_profile(user_id, profile_data)
    
    @staticmethod
    def delete_profile(user_id: str) -> bool:
        """Delete profile"""
        return enhanced_store.delete_profile(user_id)
    
    @staticmethod
    def get_skill_graph(user_id: str) -> Optional[Dict[str, Any]]:
        """Get skill graph by user ID"""
        return enhanced_store.get_skill_graph(user_id)
    
    @staticmethod
    def save_skill_graph(user_id: str, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save skill graph data"""
        return enhanced_store.save_skill_graph(user_id, skill_data)
    
    @staticmethod
    def get_internship(internship_id: str) -> Optional[Dict[str, Any]]:
        """Get internship by ID"""
        return enhanced_store.get_internship(internship_id)
    
    @staticmethod
    def get_all_internships() -> list:
        """Get all internships"""
        return enhanced_store.get_all_internships()
    
    @staticmethod
    def save_internship(internship_id: str, internship_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save internship data (not recommended - internships are read-only)"""
        MOCK_INTERNSHIPS[internship_id] = internship_data
        return internship_data
    
    @staticmethod
    def get_project(project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID"""
        return enhanced_store.get_project(project_id)
    
    @staticmethod
    def get_user_projects(user_id: str, status: Optional[str] = None) -> list:
        """Get projects by user ID"""
        return enhanced_store.get_user_projects(user_id, status)
    
    @staticmethod
    def save_project(project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save project data"""
        return enhanced_store.save_project(project_data)
    
    @staticmethod
    def save_skill_gap_analysis(user_id: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save skill gap analysis"""
        return enhanced_store.save_skill_gap_analysis(user_id, analysis_data)
    
    @staticmethod
    def get_skill_gap_analysis(user_id: str) -> Optional[Dict[str, Any]]:
        """Get skill gap analysis by user ID"""
        return enhanced_store.get_skill_gap_analysis(user_id)
    
    @staticmethod
    def save_internship_skill_graph(graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save internship skill graph"""
        return enhanced_store.save_internship_skill_graph(graph_data)
    
    @staticmethod
    def get_internship_skill_graph() -> Optional[Dict[str, Any]]:
        """Get internship skill graph"""
        return enhanced_store.get_internship_skill_graph()
    
    @staticmethod
    def save_personalized_suggestions(user_id: str, suggestions_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save personalized project suggestions"""
        return enhanced_store.save_personalized_suggestions(user_id, suggestions_data)
    
    @staticmethod
    def get_personalized_suggestions(user_id: str) -> Optional[Dict[str, Any]]:
        """Get personalized project suggestions by user ID"""
        return enhanced_store.get_personalized_suggestions(user_id)
    
    @staticmethod
    def save_career_roadmap(roadmap_id: str, roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save career roadmap"""
        return enhanced_store.save_career_roadmap(roadmap_id, roadmap_data)
    
    @staticmethod
    def get_career_roadmap(roadmap_id: str) -> Optional[Dict[str, Any]]:
        """Get career roadmap by ID"""
        return enhanced_store.get_career_roadmap(roadmap_id)
    
    @staticmethod
    def get_user_roadmaps(user_id: str) -> list:
        """Get all roadmaps for a user"""
        return enhanced_store.get_user_roadmaps(user_id)
    
    @staticmethod
    def save_explanation(cache_key: str, explanation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save explanation to cache"""
        return enhanced_store.save_explanation(cache_key, explanation_data)
    
    @staticmethod
    def get_explanation(cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached explanation"""
        return enhanced_store.get_explanation(cache_key)
    
    @staticmethod
    def clear_all():
        """Clear all mock data (useful for testing)"""
        enhanced_store.clear_all()
    
    @staticmethod
    def get_stats():
        """Get storage statistics"""
        return enhanced_store.get_stats()


# Export singleton instance
mock_store = MockStore()
