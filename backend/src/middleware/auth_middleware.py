"""Authentication middleware for FastAPI"""

from typing import Optional
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.auth import extract_user_from_token
from src.models.user import UserRole


security = HTTPBearer()


class AuthMiddleware:
    """Authentication middleware for protecting routes"""
    
    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials) -> dict:
        """
        Extract and validate user from JWT token
        
        Args:
            credentials: HTTP authorization credentials
            
        Returns:
            User info dict with user_id and role
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        token = credentials.credentials
        
        user_info = extract_user_from_token(token)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_info
    
    @staticmethod
    def require_auth(credentials: HTTPAuthorizationCredentials) -> dict:
        """
        Require authentication for route
        
        Args:
            credentials: HTTP authorization credentials
            
        Returns:
            User info dict
        """
        return AuthMiddleware.get_current_user(credentials)
    
    @staticmethod
    def require_student(credentials: HTTPAuthorizationCredentials) -> dict:
        """
        Require student role for route
        
        Args:
            credentials: HTTP authorization credentials
            
        Returns:
            User info dict
            
        Raises:
            HTTPException: If user is not a student
        """
        user_info = AuthMiddleware.get_current_user(credentials)
        
        if user_info["role"] != UserRole.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student access required"
            )
        
        return user_info
    
    @staticmethod
    def require_admin(credentials: HTTPAuthorizationCredentials) -> dict:
        """
        Require admin role for route
        
        Args:
            credentials: HTTP authorization credentials
            
        Returns:
            User info dict
            
        Raises:
            HTTPException: If user is not an admin
        """
        user_info = AuthMiddleware.get_current_user(credentials)
        
        if user_info["role"] != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        return user_info
    
    @staticmethod
    def verify_user_access(credentials: HTTPAuthorizationCredentials, user_id: str) -> dict:
        """
        Verify user can only access their own data
        
        Args:
            credentials: HTTP authorization credentials
            user_id: User ID being accessed
            
        Returns:
            User info dict
            
        Raises:
            HTTPException: If user tries to access another user's data
        """
        user_info = AuthMiddleware.get_current_user(credentials)
        
        # Admins can access any user's data
        if user_info["role"] == UserRole.ADMIN:
            return user_info
        
        # Students can only access their own data
        if user_info["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own data"
            )
        
        return user_info


# Dependency functions for FastAPI
from fastapi import Depends

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """FastAPI dependency for getting current user"""
    return AuthMiddleware.get_current_user(credentials)


def require_student(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """FastAPI dependency for requiring student role"""
    return AuthMiddleware.require_student(credentials)


def require_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """FastAPI dependency for requiring admin role"""
    return AuthMiddleware.require_admin(credentials)
