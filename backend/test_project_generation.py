"""Test project generation with Groq API"""

import asyncio
from src.services.ai_service import ai_service


async def test_project_generation():
    print("\n" + "="*60)
    print("TESTING PROJECT GENERATION WITH GROQ API")
    print("="*60 + "\n")
    
    try:
        # Test project generation
        print("Generating project for Python (intermediate level)...")
        print("-" * 60)
        
        project = await ai_service.generate_project(
            target_skills=["Python", "FastAPI"],
            student_level="intermediate"
        )
        
        if project:
            print("✅ Project Generated Successfully!\n")
            print(f"Title: {project.get('title')}")
            print(f"Description: {project.get('description')}")
            print(f"\nObjectives:")
            for obj in project.get('objectives', []):
                print(f"  - {obj}")
            print(f"\nTech Stack:")
            for tech in project.get('techStack', []):
                print(f"  - {tech.get('technology')} ({tech.get('category')}): {tech.get('purpose')}")
            print(f"\nMilestones: {len(project.get('milestones', []))}")
            for milestone in project.get('milestones', []):
                print(f"  {milestone.get('order')}. {milestone.get('title')} - {milestone.get('estimatedHours')}h")
            print(f"\nEstimated Duration: {project.get('estimatedDuration')}")
            print(f"Difficulty: {project.get('difficulty')}")
            
            print("\n" + "="*60)
            print("✅ PROJECT GENERATION TEST PASSED")
            print("="*60 + "\n")
        else:
            print("❌ Project generation returned None")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_project_generation())
