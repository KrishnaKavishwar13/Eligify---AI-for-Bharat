"""Assessment service for generating and evaluating skill-based quizzes using Groq API"""

import json
import logging
from typing import List, Dict, Any
import httpx

from src.config.settings import settings
from src.utils.errors import AIServiceError, ServiceUnavailableError

logger = logging.getLogger(__name__)

# Groq API configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = settings.GROQ_API_KEY
GROQ_MODEL = settings.GROQ_MODEL


class AssessmentService:
    """Service for generating and evaluating skill assessments"""
    
    @staticmethod
    async def call_groq(prompt: str, temperature: float = 0.7) -> str:
        """Call Groq API for question generation"""
        if not GROQ_API_KEY:
            logger.error("GROQ_API_KEY not configured")
            raise ServiceUnavailableError(
                "Groq",
                "Groq API key not configured. Please set GROQ_API_KEY in .env file"
            )
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    GROQ_API_URL,
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": GROQ_MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an expert quiz generator. You create high-quality, skill-based assessment questions with multiple choice options. Always return valid JSON."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": temperature,
                        "max_tokens": 2000,
                        "response_format": {"type": "json_object"}
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if not generated_text:
                        raise AIServiceError("AI service returned empty response")
                    return generated_text
                else:
                    error_msg = f"Groq API error: {response.status_code}"
                    logger.error(f"{error_msg} - {response.text}")
                    raise AIServiceError(error_msg)
                    
        except httpx.ConnectError as e:
            logger.error(f"Groq connection failed: {e}")
            raise ServiceUnavailableError("Groq", "AI service is not available")
        except httpx.TimeoutException as e:
            logger.error(f"Groq request timed out: {e}")
            raise AIServiceError("AI service request timed out")
        except Exception as e:
            logger.error(f"Unexpected error calling Groq: {e}")
            raise AIServiceError(f"Unexpected AI service error: {str(e)}")
    
    @staticmethod
    async def generate_questions(
        skill: str,
        difficulty: str = "intermediate",
        num_questions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate skill-based quiz questions using Groq AI
        
        Args:
            skill: The skill to test
            difficulty: beginner, intermediate, or advanced
            num_questions: Number of questions to generate
            
        Returns:
            List of questions with options and correct answers
        """
        prompt = f"""Generate {num_questions} multiple-choice questions to assess knowledge of "{skill}" at {difficulty} level.

Requirements:
- Questions should test practical understanding, not just theory
- Each question must have exactly 4 options
- Only ONE option should be correct
- Include a brief explanation for the correct answer
- Questions should be clear and unambiguous
- Difficulty: {difficulty}

Return ONLY valid JSON in this exact format:
{{
  "questions": [
    {{
      "id": 1,
      "question": "Question text here?",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": 0,
      "explanation": "Brief explanation why this is correct"
    }}
  ]
}}

The correct_answer is the index (0-3) of the correct option.
Generate {num_questions} questions about {skill}."""

        try:
            response_text = await AssessmentService.call_groq(prompt, temperature=0.7)
            
            # Parse JSON response
            response_text = response_text.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            result = json.loads(response_text.strip())
            questions = result.get("questions", [])
            
            # Validate questions
            validated_questions = []
            for i, q in enumerate(questions[:num_questions]):
                if all(key in q for key in ["question", "options", "correct_answer"]):
                    validated_questions.append({
                        "id": i + 1,
                        "question": q["question"],
                        "options": q["options"][:4],  # Ensure exactly 4 options
                        "correct_answer": q["correct_answer"],
                        "explanation": q.get("explanation", "")
                    })
            
            if not validated_questions:
                # Fallback to template questions
                return AssessmentService._generate_fallback_questions(skill, num_questions)
            
            logger.info(f"Generated {len(validated_questions)} questions for {skill}")
            return validated_questions
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return AssessmentService._generate_fallback_questions(skill, num_questions)
        except Exception as e:
            logger.error(f"Question generation error: {e}")
            return AssessmentService._generate_fallback_questions(skill, num_questions)
    
    @staticmethod
    def _generate_fallback_questions(skill: str, num_questions: int) -> List[Dict[str, Any]]:
        """Generate template-based questions when AI is unavailable"""
        templates = [
            {
                "question": f"What is a fundamental concept in {skill}?",
                "options": [
                    "Basic principles and core concepts",
                    "Advanced optimization techniques",
                    "Legacy system maintenance",
                    "Unrelated technology"
                ],
                "correct_answer": 0,
                "explanation": f"Understanding basic principles is essential for {skill}"
            },
            {
                "question": f"Which is a common use case for {skill}?",
                "options": [
                    "Solving real-world problems",
                    "Decorative purposes only",
                    "Avoiding best practices",
                    "Ignoring documentation"
                ],
                "correct_answer": 0,
                "explanation": f"{skill} is primarily used to solve practical problems"
            },
            {
                "question": f"What is an important best practice when working with {skill}?",
                "options": [
                    "Ignoring code quality",
                    "Writing clean, maintainable code",
                    "Avoiding testing",
                    "Using deprecated features"
                ],
                "correct_answer": 1,
                "explanation": "Clean, maintainable code is a universal best practice"
            },
            {
                "question": f"How would you effectively learn {skill}?",
                "options": [
                    "Only reading theory",
                    "Memorizing without practice",
                    "Building hands-on projects",
                    "Avoiding community resources"
                ],
                "correct_answer": 2,
                "explanation": "Hands-on practice is the most effective way to learn"
            },
            {
                "question": f"What makes {skill} valuable in the job market?",
                "options": [
                    "It's rarely used",
                    "It solves industry problems",
                    "It's only for beginners",
                    "It has no applications"
                ],
                "correct_answer": 1,
                "explanation": f"{skill} is valuable because it addresses real industry needs"
            }
        ]
        
        return [
            {
                "id": i + 1,
                **templates[i % len(templates)]
            }
            for i in range(num_questions)
        ]
    
    @staticmethod
    async def evaluate_quiz(
        skill: str,
        questions: List[Dict[str, Any]],
        answers: List[int]
    ) -> Dict[str, Any]:
        """
        Evaluate quiz answers and provide detailed feedback
        
        Args:
            skill: The skill being tested
            questions: List of questions with correct answers
            answers: User's answers (indices)
            
        Returns:
            Quiz results with score, feedback, and explanations
        """
        if len(questions) != len(answers):
            raise ValueError("Number of answers must match number of questions")
        
        # Calculate score
        correct_count = 0
        correct_answers = []
        explanations = []
        
        for i, (question, user_answer) in enumerate(zip(questions, answers)):
            correct_answer = question.get("correct_answer", 0)
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            correct_answers.append(correct_answer)
            explanations.append(question.get("explanation", ""))
        
        total_questions = len(questions)
        percentage = (correct_count / total_questions) * 100
        passed = percentage >= 60  # 60% passing threshold
        
        # Generate personalized feedback using Groq
        try:
            feedback = await AssessmentService._generate_feedback(
                skill=skill,
                score=correct_count,
                total=total_questions,
                percentage=percentage,
                passed=passed
            )
        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            feedback = AssessmentService._get_fallback_feedback(percentage, passed)
        
        return {
            "score": correct_count,
            "total_questions": total_questions,
            "percentage": round(percentage, 1),
            "passed": passed,
            "correct_answers": correct_answers,
            "explanations": explanations,
            "feedback": feedback
        }
    
    @staticmethod
    async def _generate_feedback(
        skill: str,
        score: int,
        total: int,
        percentage: float,
        passed: bool
    ) -> str:
        """Generate personalized feedback using Groq AI"""
        prompt = f"""Generate encouraging feedback for a student who scored {score}/{total} ({percentage:.1f}%) on a {skill} assessment.

Status: {"PASSED" if passed else "NEEDS IMPROVEMENT"}

Requirements:
- Be encouraging and constructive
- Provide specific next steps
- Keep it concise (2-3 sentences)
- Focus on growth mindset

Return ONLY JSON:
{{
  "feedback": "Your personalized feedback here"
}}"""

        try:
            response_text = await AssessmentService.call_groq(prompt, temperature=0.8)
            result = json.loads(response_text.strip())
            return result.get("feedback", AssessmentService._get_fallback_feedback(percentage, passed))
        except:
            return AssessmentService._get_fallback_feedback(percentage, passed)
    
    @staticmethod
    def _get_fallback_feedback(percentage: float, passed: bool) -> str:
        """Get template-based feedback"""
        if percentage >= 90:
            return "Excellent work! You have a strong grasp of this skill. Keep building on this foundation with advanced projects."
        elif percentage >= 75:
            return "Great job! You're doing well. Review the areas you missed and continue practicing to master this skill."
        elif percentage >= 60:
            return "Good effort! You passed the assessment. Focus on strengthening the concepts you found challenging."
        elif percentage >= 40:
            return "You're making progress! Review the fundamentals and try some beginner projects to build confidence."
        else:
            return "Keep learning! Start with foundational concepts and practice with simple projects. You'll improve with consistent effort."


# Export singleton
assessment_service = AssessmentService()
