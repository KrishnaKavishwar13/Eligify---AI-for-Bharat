"""Enhanced data store with persistence and indexing for better performance"""

from typing import Dict, Any, Optional, List
import json
from pathlib import Path
from datetime import datetime
import threading
from collections import defaultdict

# Data directory
DATA_DIR = Path(__file__).parent.parent.parent / "data"
PERSISTENCE_DIR = DATA_DIR / "persistence"
PERSISTENCE_DIR.mkdir(parents=True, exist_ok=True)

# Thread-safe lock for concurrent access
_lock = threading.RLock()


class EnhancedStore:
    """Enhanced data store with persistence, indexing, and caching"""
    
    def __init__(self):
        # In-memory storage with indexes
        self._users: Dict[str, Any] = {}
        self._profiles: Dict[str, Any] = {}
        self._skills: Dict[str, Any] = {}
        self._projects: Dict[str, Any] = {}
        self._skill_gap_analyses: Dict[str, Any] = {}
        self._personalized_suggestions: Dict[str, Any] = {}
        self._career_roadmaps: Dict[str, Any] = {}
        self._explanation_cache: Dict[str, Any] = {}
        self._internship_skill_graph: Optional[Dict[str, Any]] = None
        
        # Internships (loaded from seed data, read-only)
        self._internships: Dict[str, Any] = {}
        
        # Indexes for fast lookups
        self._user_email_index: Dict[str, str] = {}  # email -> user_id
        self._project_user_index: Dict[str, List[str]] = defaultdict(list)  # user_id -> [project_ids]
        
        # Load persisted data
        self._load_all()
        
        # Load internships from seed data
        self._load_internships()
    
    def _load_internships(self):
        """Load internships from seed data file"""
        internships_file = DATA_DIR / "internships.json"
        if internships_file.exists():
            with open(internships_file, "r", encoding="utf-8") as f:
                internships_list = json.load(f)
                self._internships = {i["internshipId"]: i for i in internships_list}
    
    def _load_all(self):
        """Load all persisted data from disk"""
        with _lock:
            self._load_collection("users", self._users, self._user_email_index)
            self._load_collection("profiles", self._profiles)
            self._load_collection("skills", self._skills)
            self._load_collection("projects", self._projects, index=self._project_user_index)
            self._load_collection("skill_gap_analyses", self._skill_gap_analyses)
            self._load_collection("personalized_suggestions", self._personalized_suggestions)
            self._load_collection("career_roadmaps", self._career_roadmaps)
    
    def _load_collection(self, name: str, target: Dict, index: Optional[Dict] = None):
        """Load a collection from disk"""
        file_path = PERSISTENCE_DIR / f"{name}.json"
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    target.update(data)
                    
                    # Build indexes
                    if index is not None and name == "users":
                        for user_id, user_data in data.items():
                            if "email" in user_data:
                                index[user_data["email"]] = user_id
                    elif index is not None and name == "projects":
                        for project_id, project_data in data.items():
                            if "userId" in project_data:
                                index[project_data["userId"]].append(project_id)
            except Exception as e:
                print(f"Warning: Failed to load {name}: {e}")
    
    def _save_collection(self, name: str, data: Dict):
        """Save a collection to disk"""
        file_path = PERSISTENCE_DIR / f"{name}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Failed to save {name}: {e}")
    
    # User operations
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        with _lock:
            return self._users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email (indexed lookup)"""
        with _lock:
            user_id = self._user_email_index.get(email)
            return self._users.get(user_id) if user_id else None
    
    def get_user_id_by_email(self, email: str) -> Optional[str]:
        """Get user ID by email (indexed lookup)"""
        with _lock:
            return self._user_email_index.get(email)
    
    def save_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save user data with persistence"""
        with _lock:
            self._users[user_id] = user_data
            if "email" in user_data:
                self._user_email_index[user_data["email"]] = user_id
            self._save_collection("users", self._users)
            return user_data
    
    # Profile operations
    def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get profile by user ID"""
        with _lock:
            return self._profiles.get(user_id)
    
    def save_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save profile data with persistence"""
        with _lock:
            self._profiles[user_id] = profile_data
            self._save_collection("profiles", self._profiles)
            return profile_data
    
    def delete_profile(self, user_id: str) -> bool:
        """Delete profile"""
        with _lock:
            if user_id in self._profiles:
                del self._profiles[user_id]
                self._save_collection("profiles", self._profiles)
                return True
            return False
    
    # Skill operations
    def get_skill_graph(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get skill graph by user ID"""
        with _lock:
            return self._skills.get(user_id)
    
    def save_skill_graph(self, user_id: str, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save skill graph data with persistence"""
        with _lock:
            self._skills[user_id] = skill_data
            self._save_collection("skills", self._skills)
            return skill_data
    
    # Internship operations (read-only from seed data)
    def get_internship(self, internship_id: str) -> Optional[Dict[str, Any]]:
        """Get internship by ID"""
        with _lock:
            return self._internships.get(internship_id)
    
    def get_all_internships(self) -> List[Dict[str, Any]]:
        """Get all internships (cached)"""
        with _lock:
            return list(self._internships.values())
    
    def search_internships(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search internships with filters (optimized)"""
        with _lock:
            results = list(self._internships.values())
            
            # Apply filters
            if "type" in filters and filters["type"]:
                results = [i for i in results if i.get("type") == filters["type"]]
            
            if "location" in filters and filters["location"]:
                location = filters["location"].lower()
                results = [i for i in results if location in i.get("location", "").lower()]
            
            if "minStipend" in filters and filters["minStipend"]:
                min_stipend = filters["minStipend"]
                results = [i for i in results if i.get("stipend", 0) >= min_stipend]
            
            return results
    
    # Project operations with indexing
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID"""
        with _lock:
            return self._projects.get(project_id)
    
    def get_user_projects(self, user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get projects by user ID (indexed lookup)"""
        with _lock:
            project_ids = self._project_user_index.get(user_id, [])
            user_projects = [self._projects[pid] for pid in project_ids if pid in self._projects]
            
            if status:
                user_projects = [p for p in user_projects if p.get("status") == status]
            
            return user_projects
    
    def save_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save project data with persistence and indexing"""
        with _lock:
            project_id = project_data.get("projectId")
            if not project_id:
                raise ValueError("Project must have projectId")
            
            user_id = project_data.get("userId")
            if not user_id:
                raise ValueError("Project must have userId")
            
            self._projects[project_id] = project_data
            
            # Update index
            if project_id not in self._project_user_index[user_id]:
                self._project_user_index[user_id].append(project_id)
            
            self._save_collection("projects", self._projects)
            return project_data
    
    # Analysis operations
    def save_skill_gap_analysis(self, user_id: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save skill gap analysis with persistence"""
        with _lock:
            self._skill_gap_analyses[user_id] = analysis_data
            self._save_collection("skill_gap_analyses", self._skill_gap_analyses)
            return analysis_data
    
    def get_skill_gap_analysis(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get skill gap analysis by user ID"""
        with _lock:
            return self._skill_gap_analyses.get(user_id)
    
    # Internship skill graph
    def save_internship_skill_graph(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save internship skill graph"""
        with _lock:
            self._internship_skill_graph = graph_data
            file_path = PERSISTENCE_DIR / "internship_skill_graph.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(graph_data, f, indent=2, ensure_ascii=False)
            return graph_data
    
    def get_internship_skill_graph(self) -> Optional[Dict[str, Any]]:
        """Get internship skill graph"""
        with _lock:
            return self._internship_skill_graph
    
    # Personalized suggestions
    def save_personalized_suggestions(self, user_id: str, suggestions_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save personalized project suggestions with persistence"""
        with _lock:
            self._personalized_suggestions[user_id] = suggestions_data
            self._save_collection("personalized_suggestions", self._personalized_suggestions)
            return suggestions_data
    
    def get_personalized_suggestions(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get personalized project suggestions by user ID"""
        with _lock:
            return self._personalized_suggestions.get(user_id)
    
    # Career roadmaps
    def save_career_roadmap(self, roadmap_id: str, roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save career roadmap with persistence"""
        with _lock:
            self._career_roadmaps[roadmap_id] = roadmap_data
            self._save_collection("career_roadmaps", self._career_roadmaps)
            return roadmap_data
    
    def get_career_roadmap(self, roadmap_id: str) -> Optional[Dict[str, Any]]:
        """Get career roadmap by ID"""
        with _lock:
            return self._career_roadmaps.get(roadmap_id)
    
    def get_user_roadmaps(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all roadmaps for a user"""
        with _lock:
            return [r for r in self._career_roadmaps.values() if r.get("userId") == user_id]
    
    # Explanation cache
    def save_explanation(self, cache_key: str, explanation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save explanation to cache (memory only, no persistence)"""
        with _lock:
            self._explanation_cache[cache_key] = explanation_data
            return explanation_data
    
    def get_explanation(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached explanation"""
        with _lock:
            return self._explanation_cache.get(cache_key)
    
    # Utility operations
    def clear_all(self):
        """Clear all data (useful for testing)"""
        with _lock:
            self._users.clear()
            self._profiles.clear()
            self._skills.clear()
            self._projects.clear()
            self._skill_gap_analyses.clear()
            self._personalized_suggestions.clear()
            self._career_roadmaps.clear()
            self._explanation_cache.clear()
            self._internship_skill_graph = None
            
            # Clear indexes
            self._user_email_index.clear()
            self._project_user_index.clear()
            
            # Clear persistence files
            for file in PERSISTENCE_DIR.glob("*.json"):
                file.unlink()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        with _lock:
            return {
                "users": len(self._users),
                "profiles": len(self._profiles),
                "skills": len(self._skills),
                "internships": len(self._internships),
                "projects": len(self._projects),
                "skillGapAnalyses": len(self._skill_gap_analyses),
                "personalizedSuggestions": len(self._personalized_suggestions),
                "careerRoadmaps": len(self._career_roadmaps),
                "explanationCache": len(self._explanation_cache),
                "persistenceEnabled": True,
                "dataDirectory": str(PERSISTENCE_DIR)
            }
    
    def backup_to_file(self, backup_name: str = None):
        """Create a backup of all data"""
        if backup_name is None:
            backup_name = f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        backup_dir = DATA_DIR / "backups" / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        with _lock:
            collections = {
                "users": self._users,
                "profiles": self._profiles,
                "skills": self._skills,
                "projects": self._projects,
                "skill_gap_analyses": self._skill_gap_analyses,
                "personalized_suggestions": self._personalized_suggestions,
                "career_roadmaps": self._career_roadmaps,
            }
            
            for name, data in collections.items():
                file_path = backup_dir / f"{name}.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(backup_dir)


# Export singleton instance
enhanced_store = EnhancedStore()
