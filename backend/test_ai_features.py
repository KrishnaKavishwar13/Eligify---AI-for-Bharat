"""Quick test script for AI features"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.ai_service import ai_service


async def test_project_generation():
    """Test AI project generation"""
    print("🧪 Testing AI Project Generation...")
    print("=" * 50)
    
    target_skills = ["Docker", "Kubernetes"]
    student_level = "intermediate"
    
    print(f"Target Skills: {', '.join(target_skills)}")
    print(f"Student Level: {student_level}")
    print("\n⏳ Generating project with Ollama (this may take 30-60 seconds)...\n")
    
    try:
        result = await ai_service.generate_project(
            target_skills=target_skills,
            student_level=student_level,
            user_context=None
        )
        
        if result:
            print("✅ Project Generated Successfully!")
            print("=" * 50)
            print(f"\n📋 Title: {result.get('title')}")
            print(f"\n📝 Description: {result.get('description')}")
            print(f"\n🎯 Objectives:")
            for obj in result.get('objectives', []):
                print(f"   • {obj}")
            print(f"\n🛠️  Tech Stack:")
            for tech in result.get('techStack', []):
                print(f"   • {tech.get('technology')} ({tech.get('category')})")
            print(f"\n📅 Milestones: {len(result.get('milestones', []))}")
            for milestone in result.get('milestones', []):
                print(f"   {milestone.get('order')}. {milestone.get('title')} - {milestone.get('estimatedHours')}h")
            print(f"\n⏱️  Duration: {result.get('estimatedDuration')}")
            print("\n" + "=" * 50)
        else:
            print("❌ Project generation failed - no result returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def test_ollama_connection():
    """Test basic Ollama connection"""
    print("🧪 Testing Ollama Connection...")
    print("=" * 50)
    
    try:
        response = await ai_service.call_ollama("Say 'Hello' in JSON format: {\"message\": \"Hello\"}", temperature=0.1)
        if response:
            print("✅ Ollama is responding!")
            print(f"Response: {response[:200]}")
        else:
            print("❌ Ollama returned empty response")
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")


async def main():
    """Run all tests"""
    print("\n🚀 Eligify AI Features Test Suite")
    print("=" * 50)
    print()
    
    # Test 1: Ollama connection
    await test_ollama_connection()
    print("\n")
    
    # Test 2: Project generation
    await test_project_generation()
    print("\n")
    
    print("✨ Testing complete!")


if __name__ == "__main__":
    asyncio.run(main())
