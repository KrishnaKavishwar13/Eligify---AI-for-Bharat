import asyncio
import sys
sys.path.insert(0, 'backend/src')

from services.ai_service import ai_service

# Sample resume text
resume_text = """
RUDRA DEWATWAL
Software Engineer
Email: rudra@example.com | Phone: +91-9876543210

SKILLS
- Programming: Python, JavaScript, TypeScript, Java
- Web Development: React, Node.js, Express, Next.js
- Databases: MongoDB, PostgreSQL, MySQL
- Tools: Git, Docker, AWS
- Soft Skills: Communication, Team Collaboration, Problem Solving

EXPERIENCE
Frontend Developer Intern at TechStart India (Jun 2025 - Aug 2025)
- Built responsive web applications using React and TypeScript
- Implemented user authentication and dashboard features

EDUCATION
Bachelor of Technology in Computer Science
Indian Institute of Technology, Mumbai (2023-2027)
CGPA: 8.5/10
"""

async def test_extraction():
    print("Testing AI skill extraction...")
    print("=" * 50)
    
    result = await ai_service.extract_skills_from_resume(resume_text)
    
    print(f"\nResult type: {type(result)}")
    print(f"Result: {result}")
    print(f"\nSkills extracted: {len(result.get('skills', []))}")
    
    if result.get('skills'):
        print("\nExtracted skills:")
        for skill in result['skills']:
            print(f"  - {skill}")

if __name__ == "__main__":
    asyncio.run(test_extraction())
