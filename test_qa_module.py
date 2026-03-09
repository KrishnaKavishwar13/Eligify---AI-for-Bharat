"""Test script for QA module with Groq API"""

import asyncio
import sys
sys.path.insert(0, 'backend')

from src.services.assessment_service import assessment_service


async def test_generate_questions():
    """Test question generation"""
    print("=" * 60)
    print("Testing Question Generation")
    print("=" * 60)
    
    try:
        questions = await assessment_service.generate_questions(
            skill="Python",
            difficulty="intermediate",
            num_questions=3
        )
        
        print(f"\n✅ Successfully generated {len(questions)} questions\n")
        
        for i, q in enumerate(questions, 1):
            print(f"Question {i}:")
            print(f"  Q: {q['question']}")
            print(f"  Options:")
            for j, opt in enumerate(q['options']):
                marker = "✓" if j == q['correct_answer'] else " "
                print(f"    [{marker}] {j}. {opt}")
            print(f"  Explanation: {q.get('explanation', 'N/A')}")
            print()
        
        return questions
        
    except Exception as e:
        print(f"\n❌ Error generating questions: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_evaluate_quiz(questions):
    """Test quiz evaluation"""
    print("=" * 60)
    print("Testing Quiz Evaluation")
    print("=" * 60)
    
    if not questions:
        print("❌ No questions to evaluate")
        return
    
    try:
        # Simulate user answers (mix of correct and incorrect)
        answers = [q['correct_answer'] if i % 2 == 0 else (q['correct_answer'] + 1) % 4 
                   for i, q in enumerate(questions)]
        
        print(f"\nSimulated answers: {answers}")
        print(f"Correct answers: {[q['correct_answer'] for q in questions]}\n")
        
        result = await assessment_service.evaluate_quiz(
            skill="Python",
            questions=questions,
            answers=answers
        )
        
        print("✅ Quiz Evaluation Results:")
        print(f"  Score: {result['score']}/{result['total_questions']}")
        print(f"  Percentage: {result['percentage']}%")
        print(f"  Status: {'PASSED ✓' if result['passed'] else 'NEEDS IMPROVEMENT'}")
        print(f"\n  Feedback: {result['feedback']}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error evaluating quiz: {e}")
        import traceback
        traceback.print_exc()


async def test_groq_connection():
    """Test Groq API connection"""
    print("=" * 60)
    print("Testing Groq API Connection")
    print("=" * 60)
    
    try:
        from src.config.settings import settings
        
        if not settings.GROQ_API_KEY:
            print("❌ GROQ_API_KEY not configured in .env")
            return False
        
        print(f"✅ GROQ_API_KEY configured")
        print(f"✅ Model: {settings.GROQ_MODEL}")
        
        # Test API call
        response = await assessment_service.call_groq(
            "Return JSON: {\"test\": \"success\"}",
            temperature=0.1
        )
        
        print(f"✅ Groq API connection successful")
        print(f"   Response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Groq API connection failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("QA MODULE TEST SUITE")
    print("=" * 60 + "\n")
    
    # Test 1: Groq connection
    groq_ok = await test_groq_connection()
    print()
    
    if not groq_ok:
        print("⚠️  Groq API not available. Tests will use fallback templates.")
        print()
    
    # Test 2: Generate questions
    questions = await test_generate_questions()
    
    # Test 3: Evaluate quiz
    if questions:
        await test_evaluate_quiz(questions)
    
    print("=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
