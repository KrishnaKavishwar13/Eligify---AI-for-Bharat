"""Test script for skills extraction with Groq (primary) and Ollama (fallback)"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.ai_service import AIService

# Sample resume text
SAMPLE_RESUME = """
John Doe
Software Engineer

EXPERIENCE:
- 3+ years of Python development
- Expert in React and Node.js
- 2 years experience with Docker and AWS
- Intermediate knowledge of PostgreSQL

SKILLS:
- Programming: Python, JavaScript, TypeScript, Java
- Frameworks: React, Django, FastAPI, Express.js
- Tools: Git, Docker, Kubernetes, Jenkins
- Databases: PostgreSQL, MongoDB, Redis
- Soft Skills: Team Leadership, Agile Methodology, Communication

PROJECTS:
- Built microservices architecture using FastAPI
- Developed React dashboard with real-time analytics
- Implemented CI/CD pipeline with Jenkins and Docker
"""

async def test_skills_extraction():
    """Test skills extraction with Groq primary and Ollama fallback"""
    print("=" * 60)
    print("Testing Skills Extraction")
    print("=" * 60)
    print("\nSample Resume:")
    print("-" * 60)
    print(SAMPLE_RESUME[:300] + "...")
    print("-" * 60)
    
    try:
        print("\n🔄 Extracting skills (Groq primary, Ollama fallback)...")
        result = await AIService.extract_skills_from_resume(SAMPLE_RESUME)
        
        skills = result.get("skills", [])
        
        if not skills:
            print("\n❌ No skills extracted!")
            return False
        
        print(f"\n✅ Successfully extracted {len(skills)} skills!")
        print("\nExtracted Skills:")
        print("-" * 60)
        
        # Group by category
        by_category = {}
        for skill in skills:
            category = skill.get("category", "unknown")
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(skill)
        
        for category, category_skills in sorted(by_category.items()):
            print(f"\n{category.upper().replace('_', ' ')}:")
            for skill in category_skills:
                name = skill.get("name", "Unknown")
                proficiency = skill.get("proficiency", 0)
                print(f"  • {name} (Proficiency: {proficiency})")
        
        print("\n" + "=" * 60)
        print("✅ Skills extraction test PASSED")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error during skills extraction: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_skills_extraction())
    sys.exit(0 if success else 1)
