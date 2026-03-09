"""Assessment/Quiz handler for skill-based questions"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.middleware.auth_middleware import get_current_user
from src.services.assessment_service import assessment_service
from src.utils.errors import AppError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/assessment", tags=["assessment"])


class GenerateQuestionsRequest(BaseModel):
    """Request model for generating questions"""
    skill: str
    difficulty: str = "intermediate"  # beginner, intermediate, advanced
    num_questions: int = 5


class QuestionOption(BaseModel):
    """Question option model"""
    text: str
    is_correct: bool


class Question(BaseModel):
    """Question model"""
    id: int
    question: str
    options: List[str]
    correct_answer: int
    explanation: str


class GenerateQuestionsResponse(BaseModel):
    """Response model for generated questions"""
    success: bool = True
    data: dict
    message: str = "Questions generated successfully"


class SubmitAnswersRequest(BaseModel):
    """Request model for submitting quiz answers"""
    skill: str
    questions: List[dict]
    answers: List[int]


class QuizResult(BaseModel):
    """Quiz result model"""
    score: int
    total_questions: int
    percentage: float
    passed: bool
    correct_answers: List[int]
    explanations: List[str]
    feedback: str


class SubmitAnswersResponse(BaseModel):
    """Response model for quiz evaluation"""
    success: bool = True
    data: QuizResult
    message: str = "Quiz evaluated successfully"


@router.post("/generate-questions", response_model=GenerateQuestionsResponse)
async def generate_questions(
    request: GenerateQuestionsRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate skill-based quiz questions using Groq AI
    
    Args:
        request: Question generation parameters
        current_user: Authenticated user
        
    Returns:
        Generated questions with options
    """
    try:
        user_id = current_user.get("user_id")
        logger.info(f"Generating {request.num_questions} questions for skill: {request.skill}, difficulty: {request.difficulty}")
        
        # Generate questions using AI
        questions = await assessment_service.generate_questions(
            skill=request.skill,
            difficulty=request.difficulty,
            num_questions=request.num_questions
        )
        
        return GenerateQuestionsResponse(
            data={
                "skill": request.skill,
                "difficulty": request.difficulty,
                "questions": questions
            },
            message=f"Generated {len(questions)} questions for {request.skill}"
        )
        
    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error generating questions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate questions"
        )


@router.post("/evaluate-quiz", response_model=SubmitAnswersResponse)
async def evaluate_quiz(
    request: SubmitAnswersRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Evaluate quiz answers and provide feedback
    
    Args:
        request: Quiz answers
        current_user: Authenticated user
        
    Returns:
        Quiz results with score and feedback
    """
    try:
        user_id = current_user.get("user_id")
        logger.info(f"Evaluating quiz for user {user_id}, skill: {request.skill}")
        
        # Evaluate quiz
        result = await assessment_service.evaluate_quiz(
            skill=request.skill,
            questions=request.questions,
            answers=request.answers
        )
        
        return SubmitAnswersResponse(
            data=result,
            message="Quiz evaluated successfully"
        )
        
    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error evaluating quiz: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to evaluate quiz"
        )
