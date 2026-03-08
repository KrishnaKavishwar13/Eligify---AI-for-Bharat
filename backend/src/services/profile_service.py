"""Profile service for student profile management"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4

from src.config.settings import settings
from src.models.user import StudentProfile, PersonalInfo, UserRole
from src.models.skill import SkillNode, SkillGraph, SkillStatus, SkillCategory, SkillSource
from src.utils.dynamodb import get_item, put_item, update_item, delete_item
from src.services.ai_service import ai_service

logger = logging.getLogger(__name__)
from src.utils.s3 import upload_file, generate_presigned_url
from src.services.ai_service import ai_service


class ProfileService:
    """Service for managing student profiles"""
    
    @staticmethod
    async def create_profile(user_id: str, profile_data: Dict[str, Any]) -> StudentProfile:
        """Create new student profile"""
        now = datetime.utcnow().isoformat()
        
        profile = StudentProfile(
            userId=user_id,
            personalInfo=PersonalInfo(**profile_data.get("personalInfo", {})),
            education=profile_data.get("education", []),
            experience=profile_data.get("experience", []),
            projects=profile_data.get("projects", []),
            certifications=profile_data.get("certifications", []),
            role=UserRole.STUDENT,
            onboardingComplete=False,
            createdAt=now,
            updatedAt=now
        )
        
        # Save to mock store
        from src.utils.mock_store import mock_store
        mock_store.save_profile(user_id, profile.dict(by_alias=True))
        return profile
    
    @staticmethod
    async def get_profile(user_id: str) -> Optional[StudentProfile]:
        """Get student profile"""
        from src.utils.mock_store import mock_store
        item = mock_store.get_profile(user_id)
        return StudentProfile(**item) if item else None
    
    @staticmethod
    async def update_profile(user_id: str, updates) -> StudentProfile:
        """Update student profile"""
        from src.utils.mock_store import mock_store
        now = datetime.utcnow().isoformat()
        
        # Get existing profile
        profile_dict = mock_store.get_profile(user_id)
        if not profile_dict:
            raise ValueError("Profile not found")
        
        # Convert ProfileUpdate model to dict if needed
        if hasattr(updates, 'dict'):
            updates_dict = updates.dict(by_alias=True, exclude_none=True)
        else:
            updates_dict = updates
        
        # Update fields
        for key, value in updates_dict.items():
            if value is not None:
                profile_dict[key] = value
        profile_dict["updatedAt"] = now
        
        # Save updated profile
        mock_store.save_profile(user_id, profile_dict)
        return StudentProfile(**profile_dict)
    
    @staticmethod
    async def upload_resume(user_id: str, file, file_content: bytes) -> Dict[str, Any]:
        """Upload resume and extract skills"""
        from src.utils.mock_store import mock_store
        from src.services.skill_service import skill_service
        from docx import Document
        from io import BytesIO
        
        # For MVP, we'll skip S3 upload and just extract skills from content
        # In production, uncomment S3 upload code below
        
        # Upload to S3 (commented out for MVP - no AWS credentials needed)
        # from io import BytesIO
        # file_obj = BytesIO(file_content)
        # s3_uri = await upload_file(file_obj, file.filename, user_id, file.content_type)
        
        # For MVP, use a mock S3 URI
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        mock_s3_uri = f"s3://eligify-resumes/resumes/{user_id}/{timestamp}-{file.filename}"
        
        # Extract text from file content based on file type
        resume_text = ""
        file_ext = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
        
        try:
            if file_ext == 'docx':
                # Extract text from DOCX
                doc = Document(BytesIO(file_content))
                resume_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                logger.info(f"Extracted {len(resume_text)} characters from DOCX")
            elif file_ext == 'txt':
                # Plain text file
                resume_text = file_content.decode('utf-8', errors='ignore')
            elif file_ext == 'pdf':
                # For PDF, try basic text extraction (in production use PyPDF2 or pdfplumber)
                resume_text = file_content.decode('latin-1', errors='ignore')
            else:
                # Fallback
                resume_text = file_content.decode('utf-8', errors='ignore')
            
            # Clean up the text
            resume_text = resume_text.replace('\x00', ' ').replace('\r', '\n')
            resume_text = ' '.join(resume_text.split())  # Normalize whitespace
            
        except Exception as e:
            logger.error(f"Error extracting text from {file_ext} file: {e}")
            resume_text = ""
        
        # If text is too short, provide a fallback
        if len(resume_text.strip()) < 50:
            logger.warning(f"Resume text too short ({len(resume_text)} chars)")
            return {
                "resumeUrl": mock_s3_uri,
                "resumeFilename": file.filename,
                "uploadedAt": datetime.utcnow().isoformat(),
                "extractedSkills": [],
                "skillsAdded": [],
                "skillsAlreadyExist": [],
                "totalSkillsExtracted": 0,
                "newSkillsAdded": 0,
                "error": "Unable to extract text from file. Please ensure your resume contains readable text."
            }
        
        # Extract skills using AI
        extracted_data = await ai_service.extract_skills_from_resume(resume_text)
        extracted_skills_data = extracted_data.get("skills", [])
        
        # Auto-add extracted skills to user's skill graph
        skills_added = []
        skills_already_exist = []
        
        if extracted_skills_data:
            # Get existing skill graph
            skill_graph = await skill_service.get_skill_graph(user_id)
            existing_skill_names = set()
            
            if skill_graph:
                existing_skill_names = {skill.name.lower() for skill in skill_graph.skills}
            
            # Add new skills
            for skill_data in extracted_skills_data:
                # Handle both dict and string formats
                if isinstance(skill_data, dict):
                    skill_name = skill_data.get("name", "")
                    proficiency = skill_data.get("proficiency", 50)
                    category = skill_data.get("category", "technical")
                else:
                    skill_name = str(skill_data)
                    proficiency = 50
                    category = "technical"
                
                if not skill_name:
                    continue
                    
                if skill_name.lower() not in existing_skill_names:
                    try:
                        # Add skill with proficiency from AI or default 50
                        await skill_service.add_skill(
                            user_id=user_id,
                            skill_name=skill_name,
                            category=category,
                            proficiency=proficiency
                        )
                        skills_added.append(skill_name)
                    except Exception as e:
                        logger.warning(f"Failed to add skill {skill_name}: {e}")
                else:
                    skills_already_exist.append(skill_name)
        
        # Update profile with resume URI
        profile_dict = mock_store.get_profile(user_id)
        if profile_dict:
            profile_dict["resumeS3Uri"] = mock_s3_uri
            profile_dict["resumeUploadedAt"] = datetime.utcnow().isoformat()
            profile_dict["updatedAt"] = datetime.utcnow().isoformat()
            mock_store.save_profile(user_id, profile_dict)
        
        # Return result with resume URL and extracted skills
        # Convert skill data to simple list for frontend
        extracted_skill_names = []
        for skill_data in extracted_skills_data:
            if isinstance(skill_data, dict):
                extracted_skill_names.append(skill_data.get("name", ""))
            else:
                extracted_skill_names.append(str(skill_data))
        
        return {
            "resumeUrl": mock_s3_uri,
            "resumeFilename": file.filename,
            "uploadedAt": datetime.utcnow().isoformat(),
            "extractedSkills": extracted_skill_names,
            "skillsAdded": skills_added,
            "skillsAlreadyExist": skills_already_exist,
            "totalSkillsExtracted": len(extracted_skill_names),
            "newSkillsAdded": len(skills_added)
        }
    
    @staticmethod
    async def delete_profile(user_id: str) -> bool:
        """Delete student profile"""
        from src.utils.mock_store import mock_store
        return mock_store.delete_profile(user_id)


profile_service = ProfileService()
