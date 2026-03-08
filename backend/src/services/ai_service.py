"""AI service with Ollama (local LLM)"""

import json
import logging
from typing import Optional, Dict, Any, List
import httpx

from src.utils.retry import retry_ollama
from src.utils.errors import AIServiceError, ServiceUnavailableError

logger = logging.getLogger(__name__)

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"


class AIService:
    """AI service for resume parsing and project generation using Ollama"""
    
    @staticmethod
    @retry_ollama(max_attempts=3)
    async def call_ollama(prompt: str, temperature: float = 0.3) -> Optional[str]:
        """
        Call Ollama API with a prompt (with automatic retry)
        
        Args:
            prompt: The prompt to send to Ollama
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            Generated text or None if failed
            
        Raises:
            ServiceUnavailableError: If Ollama is not running
            AIServiceError: If Ollama returns an error
        """
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    OLLAMA_API_URL,
                    json={
                        "model": OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": temperature,
                        "format": "json"  # Request JSON output
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get("response", "")
                    if not generated_text:
                        logger.warning("Ollama returned empty response")
                        raise AIServiceError("AI service returned empty response")
                    return generated_text
                else:
                    error_msg = f"Ollama API error: {response.status_code}"
                    logger.error(f"{error_msg} - {response.text}")
                    raise AIServiceError(
                        error_msg,
                        details={"status_code": response.status_code, "response": response.text}
                    )
                    
        except httpx.ConnectError as e:
            logger.error(f"Ollama connection failed: {e}")
            raise ServiceUnavailableError(
                "Ollama",
                "AI service is not available. Make sure Ollama is running: ollama serve"
            )
        except httpx.TimeoutException as e:
            logger.error(f"Ollama request timed out: {e}")
            raise AIServiceError(
                "AI service request timed out",
                details={"timeout": 120.0}
            )
        except Exception as e:
            logger.error(f"Unexpected error calling Ollama: {e}")
            raise AIServiceError(f"Unexpected AI service error: {str(e)}")
        except httpx.TimeoutException as e:
            print(f"Ollama request timed out: {e}")
            return None
        except Exception as e:
            print(f"Ollama call failed: {type(e).__name__}: {e}")
            return None
    
    @staticmethod
    async def extract_skills_from_resume(resume_text: str) -> Dict[str, Any]:
        """
        Extract skills from resume text using Ollama
        
        Args:
            resume_text: Extracted text from resume
            
        Returns:
            Dict with extracted skills and profile data
        """
        # Truncate resume text to avoid token limits
        resume_snippet = resume_text[:2000]
        
        # Improved prompt without specific examples
        prompt = f"""You are a skill extraction AI. Analyze this resume and extract ALL technical and soft skills mentioned.

Resume Text:
{resume_snippet}

Return ONLY a JSON object with this format (no markdown, no explanation):
{{
  "skills": [
    {{"name": "skill_name_here", "category": "category_here", "proficiency": proficiency_number}}
  ]
}}

Categories to use:
- programming_language: Python, Java, JavaScript, C++, etc.
- framework: React, Django, Spring, Angular, etc.
- tool: Git, Docker, AWS, Jenkins, etc.
- soft_skill: Communication, Leadership, Teamwork, etc.
- domain_knowledge: Machine Learning, Data Analysis, Web Development, etc.

Rules:
- Extract EVERY skill mentioned in the resume
- Estimate proficiency 0-100 based on years of experience and project complexity
- If resume mentions "2+ years" or "expert", use 80-90
- If resume mentions "1 year" or "intermediate", use 60-75
- If resume mentions "beginner" or just lists skill, use 40-55
- Return ONLY valid JSON

JSON:"""

        try:
            response_text = await AIService.call_ollama(prompt, temperature=0.2)
            
            if not response_text:
                logger.warning("AI returned empty response for resume extraction")
                return {"skills": []}
            
            # Clean response - remove markdown and extra text
            response_text = response_text.strip()
            
            # Remove markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            response_text = response_text.strip()
            
            # Try to find JSON object in response
            if "{" in response_text and "}" in response_text:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                response_text = response_text[start:end]
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Validate skills format
            skills = result.get("skills", [])
            if not isinstance(skills, list):
                logger.warning(f"Skills is not a list: {type(skills)}")
                return {"skills": []}
            
            # Ensure each skill has required fields
            validated_skills = []
            for skill in skills:
                if isinstance(skill, dict) and "name" in skill:
                    validated_skills.append({
                        "name": skill["name"],
                        "category": skill.get("category", "technical"),
                        "proficiency": skill.get("proficiency", 50)
                    })
            
            logger.info(f"Extracted {len(validated_skills)} skills from resume")
            return {"skills": validated_skills}
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Response was: {response_text[:500] if response_text else 'None'}")
            return {"skills": []}
        except Exception as e:
            logger.error(f"Resume extraction error: {e}")
            return {"skills": []}
    
    @staticmethod
    async def generate_project(
        target_skills: List[str],
        student_level: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate project roadmap using Ollama
        
        Args:
            target_skills: Skills to learn
            student_level: beginner, intermediate, or advanced
            user_context: Optional student context
            
        Returns:
            Generated project dict or None
        """
        skills_str = ", ".join(target_skills)
        
        prompt = f"""Create a project for a {student_level} student to learn: {skills_str}

Return ONLY JSON (no markdown, no explanation):
{{
  "title": "Project Title",
  "description": "What will be built and why",
  "objectives": ["Learn X", "Build Y", "Practice Z"],
  "techStack": [
    {{"category": "frontend", "technology": "React", "purpose": "UI"}},
    {{"category": "backend", "technology": "Node.js", "purpose": "API"}}
  ],
  "milestones": [
    {{
      "title": "Setup",
      "description": "Initialize project",
      "tasks": ["Setup environment", "Design schema"],
      "estimatedHours": 4,
      "order": 1
    }},
    {{
      "title": "Development",
      "description": "Build features",
      "tasks": ["Implement auth", "Create CRUD"],
      "estimatedHours": 12,
      "order": 2
    }},
    {{
      "title": "Testing",
      "description": "Test and deploy",
      "tasks": ["Write tests", "Deploy"],
      "estimatedHours": 6,
      "order": 3
    }}
  ],
  "estimatedDuration": "1-2 weeks",
  "difficulty": "intermediate",
  "resources": [
    {{"type": "documentation", "title": "React Docs", "url": "https://react.dev"}}
  ]
}}

Make it practical for learning {skills_str}. Return ONLY JSON."""

        try:
            response_text = await AIService.call_ollama(prompt, temperature=0.7)
            
            if not response_text:
                # Fallback to template-based project
                return AIService._generate_fallback_project(target_skills, student_level)
            
            # Clean response
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            result = json.loads(response_text)
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in project generation: {e}")
            print(f"Response was: {response_text[:500] if response_text else 'None'}")
            # Fallback to template-based project
            return AIService._generate_fallback_project(target_skills, student_level)
        except Exception as e:
            print(f"Project generation error: {e}")
            # Fallback to template-based project
            return AIService._generate_fallback_project(target_skills, student_level)
    
    @staticmethod
    def _generate_fallback_project(target_skills: List[str], student_level: str) -> Dict[str, Any]:
        """Generate a template-based project when AI is unavailable"""
        skills_str = ", ".join(target_skills)
        
        # Determine project complexity based on level
        hours_map = {
            "beginner": {"setup": 4, "dev": 8, "test": 4},
            "intermediate": {"setup": 6, "dev": 16, "test": 6},
            "advanced": {"setup": 8, "dev": 24, "test": 8}
        }
        hours = hours_map.get(student_level.lower(), hours_map["intermediate"])
        
        return {
            "title": f"{skills_str} Learning Project",
            "description": f"A hands-on {student_level} level project to master {skills_str} through practical implementation.",
            "objectives": [
                f"Gain practical experience with {target_skills[0] if target_skills else 'core technologies'}",
                "Build a complete, working application",
                "Apply best practices and industry standards",
                "Create portfolio-ready project"
            ],
            "techStack": [
                {"category": "core", "technology": skill, "purpose": "Primary skill"} 
                for skill in target_skills[:3]
            ],
            "milestones": [
                {
                    "title": "Project Setup & Planning",
                    "description": "Initialize project structure and plan architecture",
                    "tasks": [
                        "Set up development environment",
                        "Design system architecture",
                        "Create project structure",
                        "Initialize version control"
                    ],
                    "estimatedHours": hours["setup"],
                    "order": 1
                },
                {
                    "title": "Core Development",
                    "description": "Implement main features and functionality",
                    "tasks": [
                        "Implement core features",
                        "Build user interface",
                        "Add data persistence",
                        "Integrate APIs and services"
                    ],
                    "estimatedHours": hours["dev"],
                    "order": 2
                },
                {
                    "title": "Testing & Deployment",
                    "description": "Test thoroughly and deploy to production",
                    "tasks": [
                        "Write unit tests",
                        "Perform integration testing",
                        "Deploy to hosting platform",
                        "Document the project"
                    ],
                    "estimatedHours": hours["test"],
                    "order": 3
                }
            ],
            "estimatedDuration": f"{sum(hours.values()) // 7}-{(sum(hours.values()) // 7) + 1} weeks",
            "difficulty": student_level,
            "resources": [
                {"type": "documentation", "title": f"{target_skills[0]} Documentation", "url": "#"} 
                if target_skills else {"type": "documentation", "title": "Getting Started", "url": "#"}
            ]
        }


# Export singleton
ai_service = AIService()
