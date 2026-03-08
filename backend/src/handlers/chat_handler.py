"""Chat API handler for SkillGenie chatbot"""

import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.middleware.auth_middleware import get_current_user
from src.services.ai_service import ai_service
from src.services.profile_service import profile_service
from src.services.skill_service import skill_service
from src.services.internship_mapping_service import InternshipMappingService
from src.services.project_service import project_service
from src.utils.errors import AIServiceError, ValidationError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
internship_mapping_service = InternshipMappingService()


class ChatMessage(BaseModel):
    """Chat message model"""
    message: str = Field(..., min_length=1, max_length=1000)
    context: Optional[Dict[str, Any]] = None
    
    class Config:
        populate_by_name = True


class ChatResponse(BaseModel):
    """Chat response model"""
    success: bool = True
    response: str
    action: Optional[str] = None
    actionLabel: Optional[str] = None
    actionData: Optional[Dict[str, Any]] = None


@router.post("/message", response_model=ChatResponse)
async def send_chat_message(
    request: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    """
    Send a message to SkillGenie chatbot
    
    The chatbot can:
    - Answer questions about skills, internships, and projects
    - Provide career guidance
    - Explain eligibility and skill gaps
    - Suggest next steps
    - Navigate the platform
    
    Args:
        request: Chat message with optional context
        
    Returns:
        ChatResponse with AI-generated response and optional action
    """
    try:
        user_id = current_user["user_id"]
        message = request.message.lower().strip()
        
        logger.info(f"Chat message from user {user_id}: {message[:100]}")
        
        # Get user context
        profile = await profile_service.get_profile(user_id)
        skill_graph = await skill_service.get_skill_graph(user_id)
        projects = await project_service.get_user_projects(user_id, status_filter=None)
        
        # Build context for AI
        user_context = {
            "name": profile.personal_info.name if profile and profile.personal_info else "there",
            "total_skills": skill_graph.total_skills if skill_graph else 0,
            "verified_skills": skill_graph.verified_skills if skill_graph else 0,
            "total_projects": len(projects) if projects else 0,
        }
        
        # Build AI prompt
        prompt = f"""You are SkillGenie, an AI career companion for Eligify platform. You help students with:
- Career guidance and skill development
- Internship eligibility and matching
- Project suggestions and learning paths
- Skill gap analysis
- Platform navigation

User Context:
- Name: {user_context['name']}
- Total Skills: {user_context['total_skills']}
- Verified Skills: {user_context['verified_skills']}
- Projects: {user_context['total_projects']}

User Message: {request.message}

Respond in a friendly, helpful tone. Keep responses concise (2-3 sentences max). If the user asks about navigation, suggest the appropriate page.

Return ONLY JSON:
{{
  "response": "Your helpful response here",
  "action": "navigate|none",
  "actionLabel": "Button label if action is navigate",
  "actionRoute": "Route path if action is navigate"
}}

JSON:"""

        # Call Ollama
        try:
            response_text = await ai_service.call_ollama(prompt, temperature=0.7)
        except Exception as ollama_error:
            logger.warning(f"Ollama failed, using fallback response: {ollama_error}")
            response_text = None
        
        if not response_text:
            # Fallback responses based on message content
            fallback_response = _get_fallback_response(message, user_context)
            return ChatResponse(
                response=fallback_response["response"],
                action=fallback_response.get("action"),
                actionLabel=fallback_response.get("actionLabel"),
                actionData=fallback_response.get("actionData")
            )
        
        # Parse response
        import json
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        try:
            result = json.loads(response_text)
            
            return ChatResponse(
                response=result.get("response", "I can help you navigate and learn! What would you like to do?"),
                action=result.get("action"),
                actionLabel=result.get("actionLabel"),
                actionData={"route": result.get("actionRoute")} if result.get("actionRoute") else None
            )
        except json.JSONDecodeError:
            # Fallback to simple response
            return ChatResponse(
                response=response_text if len(response_text) < 500 else "I can help you with skills, internships, and projects. What would you like to know?",
                action=None
            )
    
    except (ValidationError, AIServiceError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat: {e}", exc_info=True)
        return ChatResponse(
            response="I encountered an error. Please try again!",
            action=None
        )



def _get_fallback_response(message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate fallback responses when Ollama is unavailable
    
    Args:
        message: User's message (lowercase)
        user_context: User context with name, skills, projects
        
    Returns:
        Dict with response, action, actionLabel, actionData
    """
    name = user_context.get("name", "there")
    
    # Greeting responses
    if any(word in message for word in ["hi", "hello", "hey", "hii"]):
        return {
            "response": f"Hi {name}! I'm SkillGenie, your AI career companion. How can I help you today?",
            "action": None
        }
    
    # Skills-related queries
    if any(word in message for word in ["skill", "learn", "improve"]):
        total_skills = user_context.get("total_skills", 0)
        verified = user_context.get("verified_skills", 0)
        return {
            "response": f"You have {total_skills} skills ({verified} verified). Want to explore internships or start a new project?",
            "action": "navigate",
            "actionLabel": "View Skills",
            "actionData": {"route": "/profile"}
        }
    
    # Internship queries
    if any(word in message for word in ["internship", "job", "opportunity", "apply"]):
        return {
            "response": "I can help you find internships that match your skills! Check out your personalized matches.",
            "action": "navigate",
            "actionLabel": "Browse Internships",
            "actionData": {"route": "/internships"}
        }
    
    # Project queries
    if any(word in message for word in ["project", "build", "practice"]):
        projects = user_context.get("total_projects", 0)
        return {
            "response": f"You have {projects} projects. Building projects is a great way to develop skills!",
            "action": "navigate",
            "actionLabel": "View Projects",
            "actionData": {"route": "/projects"}
        }
    
    # Career/guidance queries
    if any(word in message for word in ["career", "path", "roadmap", "guidance", "help"]):
        return {
            "response": "I can help you plan your career path! Start by exploring internships or building projects to fill skill gaps.",
            "action": "navigate",
            "actionLabel": "View Dashboard",
            "actionData": {"route": "/dashboard"}
        }
    
    # Profile queries
    if any(word in message for word in ["profile", "resume", "upload"]):
        return {
            "response": "Your profile helps me understand your skills better. You can update it anytime!",
            "action": "navigate",
            "actionLabel": "View Profile",
            "actionData": {"route": "/profile"}
        }
    
    # Default fallback
    return {
        "response": "I'm here to help with skills, internships, and career planning. What would you like to explore?",
        "action": None
    }
