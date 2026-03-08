"""Authentication service - Mock mode for local development"""

from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4
import hashlib

from src.config.settings import settings
from src.models.user import UserRole, AuthResult, PersonalInfo, StudentProfile
from src.models.skill import SkillGraph, SkillNode, SkillStatus, SkillCategory, SkillSource
from src.utils.auth import generate_tokens, verify_token
from src.utils.mock_store import mock_store


def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed


class AuthService:
    """Authentication service for user management (Mock mode)"""
    
    @staticmethod
    async def sign_up(email: str, password: str, name: str) -> AuthResult:
        """
        Register new user with mock store
        
        Args:
            email: User email
            password: User password
            name: User full name
            
        Returns:
            AuthResult with success status and user info
        """
        try:
            # Check if user already exists using enhanced_store's email index
            from src.utils.enhanced_store import enhanced_store
            existing_user_id = enhanced_store.get_user_id_by_email(email)
            if existing_user_id:
                return AuthResult(
                    success=False,
                    error="Email already registered"
                )
            
            # Create user ID
            user_id = str(uuid4())
            now = datetime.utcnow().isoformat()
            
            # Create user record
            user_data = {
                "user_id": user_id,
                "email": email,
                "name": name,
                "password_hash": hash_password(password),
                "role": UserRole.STUDENT.value,
                "created_at": now,
                "email_verified": True  # Auto-verify for local dev
            }
            
            mock_store.save_user(user_id, user_data)
            
            # Create default profile
            profile_data = {
                "userId": user_id,
                "personalInfo": {
                    "name": name,
                    "email": email,
                    "phone": None,
                    "location": None,
                    "linkedinUrl": None,
                    "githubUsername": None,
                    "portfolioUrl": None
                },
                "education": [],
                "experience": [],
                "projects": [],
                "certifications": [],
                "resumeS3Uri": None,
                "resumeUploadedAt": None,
                "role": UserRole.STUDENT.value,
                "onboardingComplete": False,
                "createdAt": now,
                "updatedAt": now,
                "lastLoginAt": None
            }
            
            mock_store.save_profile(user_id, profile_data)
            
            # Create empty skill graph for new users
            # This allows the onboarding flow to trigger (totalSkills === 0)
            skill_graph_data = {
                "userId": user_id,
                "skills": [],
                "totalSkills": 0,
                "verifiedSkills": 0,
                "lastUpdated": now
            }
            
            mock_store.save_skill_graph(user_id, skill_graph_data)
            
            return AuthResult(
                success=True,
                userId=user_id,
                accessToken=None,
                refreshToken=None,
                error=None
            )
            
        except Exception as e:
            return AuthResult(
                success=False,
                error=f"Signup failed: {str(e)}"
            )
    
    @staticmethod
    async def sign_in(email: str, password: str) -> AuthResult:
        """
        Authenticate user with mock store
        
        Args:
            email: User email
            password: User password
            
        Returns:
            AuthResult with tokens and user info
        """
        try:
            # Find user by email using enhanced_store's email index
            from src.utils.enhanced_store import enhanced_store
            user_id = enhanced_store.get_user_id_by_email(email)
            
            if not user_id:
                return AuthResult(
                    success=False,
                    error="Invalid email or password"
                )
            
            user = enhanced_store.get_user(user_id)
            if not user:
                return AuthResult(
                    success=False,
                    error="Invalid email or password"
                )
            
            # Verify password
            if not verify_password(password, user["password_hash"]):
                return AuthResult(
                    success=False,
                    error="Invalid email or password"
                )
            
            role = UserRole(user.get("role", UserRole.STUDENT.value))
            
            # Generate JWT tokens
            tokens = generate_tokens(user_id, role)
            
            # Update last login
            now = datetime.utcnow().isoformat()
            profile = mock_store.get_profile(user_id)
            if profile:
                profile["lastLoginAt"] = now
                mock_store.save_profile(user_id, profile)
            
            return AuthResult(
                success=True,
                userId=user_id,
                accessToken=tokens["access_token"],
                refreshToken=tokens["refresh_token"],
                idToken=None,
                error=None
            )
            
        except Exception as e:
            return AuthResult(
                success=False,
                error=f"Authentication failed: {str(e)}"
            )
    
    @staticmethod
    async def refresh_token(refresh_token: str) -> AuthResult:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            AuthResult with new access token
        """
        try:
            # Verify refresh token
            payload = verify_token(refresh_token, token_type="refresh")
            
            if not payload:
                return AuthResult(
                    success=False,
                    error="Invalid or expired refresh token"
                )
            
            user_id = payload.get("sub")
            role = UserRole(payload.get("role"))
            
            # Generate new tokens
            tokens = generate_tokens(user_id, role)
            
            return AuthResult(
                success=True,
                userId=user_id,
                accessToken=tokens["access_token"],
                refreshToken=tokens["refresh_token"],
                error=None
            )
            
        except Exception as e:
            return AuthResult(
                success=False,
                error=f"Token refresh failed: {str(e)}"
            )
    
    @staticmethod
    async def sign_out(user_id: str) -> bool:
        """
        Sign out user (invalidate session)
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful
            
        Note: In mock mode, tokens will expire naturally
        """
        return True
    
    @staticmethod
    async def get_user_info(user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from mock store
        
        Args:
            user_id: User ID
            
        Returns:
            User info dict or None
        """
        user = mock_store.get_user(user_id)
        if not user:
            return None
        
        return {
            "user_id": user_id,
            "email": user.get("email"),
            "name": user.get("name"),
            "role": user.get("role"),
            "email_verified": user.get("email_verified", True),
            "created_at": user.get("created_at")
        }


# Export singleton instance
auth_service = AuthService()
