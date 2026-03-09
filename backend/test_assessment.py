"""Test script for assessment service"""

import asyncio
from src.services.assessment_service import assessment_service


async def main():
    print("\n" + "="*60)
    print("TESTING QA MODULE WITH GROQ API")
    print("="*60 + "\n")
    
    # Test 1: Generate Questions
    print("Test 1: Generating Questions for 'Python'...")
    print("-" * 60)
    
    try:
        questions = await assessment_service.generate_questions(
            skill="Python",
            difficulty="intermediate",
            num_questions=3
        )
        
        print(f"✅ Generated {len(questions)} questions\n")
        
        for i, q in enumerate(questions, 1):
            print(f"Question {i}: {q['question']}")
            for j, opt in enumerate(q['options']):
                marker = "✓" if j == q['correct_answer'] else " "
                print(f"  [{marker}] {opt}")
            print(f"  💡 {q.get('explanation', '')}\n")
        
        # Test 2: Evaluate Quiz
        print("\nTest 2: Evaluating Quiz...")
        print("-" * 60)
        
        # Simulate answers (2 correct, 1 wrong)
        answers = [
            questions[0]['correct_answer'],  # Correct
            questions[1]['correct_answer'],  # Correct
            (questions[2]['correct_answer'] + 1) % 4  # Wrong
        ]
        
        result = await assessment_service.evaluate_quiz(
            skill="Python",
            questions=questions,
            answers=answers
        )
        
        print(f"✅ Quiz Evaluated")
        print(f"   Score: {result['score']}/{result['total_questions']}")
        print(f"   Percentage: {result['percentage']}%")
        print(f"   Status: {'PASSED ✓' if result['passed'] else 'NEEDS IMPROVEMENT'}")
        print(f"   Feedback: {result['feedback']}")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
