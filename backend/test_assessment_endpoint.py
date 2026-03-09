"""Test assessment endpoint directly"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.services.assessment_service import AssessmentService

async def test_generate_questions():
    """Test question generation"""
    print("=" * 60)
    print("Testing Assessment Question Generation")
    print("=" * 60)
    
    test_skills = ["Docker", "Kubernetes", "Python", "React"]
    
    for skill in test_skills:
        print(f"\n🔄 Generating questions for: {skill}")
        print("-" * 60)
        
        try:
            questions = await AssessmentService.generate_questions(
                skill=skill,
                difficulty="intermediate",
                num_questions=5
            )
            
            if not questions:
                print(f"❌ No questions generated for {skill}")
                continue
            
            print(f"✅ Generated {len(questions)} questions for {skill}")
            
            # Show first question as sample
            if questions:
                q = questions[0]
                print(f"\nSample Question:")
                print(f"Q: {q['question']}")
                print(f"Options:")
                for i, opt in enumerate(q['options']):
                    marker = "✓" if i == q['correct_answer'] else " "
                    print(f"  [{marker}] {i+1}. {opt}")
                print(f"Explanation: {q.get('explanation', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error generating questions for {skill}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ Assessment test completed")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_generate_questions())
