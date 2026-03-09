# Groq API Integration for QA Module

## Overview
Successfully integrated Groq API for AI-powered quiz generation and evaluation in the SkillGenie assessment module.

## Features Implemented

### 1. AI-Powered Question Generation
- **Endpoint**: `POST /assessment/generate-questions`
- **Functionality**: 
  - Generates skill-specific multiple-choice questions
  - Supports difficulty levels: beginner, intermediate, advanced
  - Creates 4 options per question with one correct answer
  - Includes explanations for correct answers
  - Configurable number of questions (default: 5)

### 2. Intelligent Quiz Evaluation
- **Endpoint**: `POST /assessment/evaluate-quiz`
- **Functionality**:
  - Evaluates user answers against correct answers
  - Calculates score and percentage
  - Determines pass/fail (60% threshold)
  - Generates personalized AI feedback
  - Provides explanations for all questions

### 3. Frontend Integration
- **Page**: `/skillgenie/assessment`
- **Features**:
  - Dynamic question loading from API
  - Interactive quiz interface
  - Real-time progress tracking
  - Detailed results with AI feedback
  - Review incorrect answers with explanations
  - Adaptive routing based on performance

## API Endpoints

### Generate Questions
```http
POST /assessment/generate-questions
Authorization: Bearer <token>
Content-Type: application/json

{
  "skill": "Python",
  "difficulty": "intermediate",
  "num_questions": 5
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "skill": "Python",
    "difficulty": "intermediate",
    "questions": [
      {
        "id": 1,
        "question": "What is a list comprehension in Python?",
        "options": [
          "A way to create lists concisely",
          "A type of loop",
          "A function decorator",
          "A class method"
        ],
        "correct_answer": 0,
        "explanation": "List comprehensions provide a concise way to create lists"
      }
    ]
  },
  "message": "Generated 5 questions for Python"
}
```

### Evaluate Quiz
```http
POST /assessment/evaluate-quiz
Authorization: Bearer <token>
Content-Type: application/json

{
  "skill": "Python",
  "questions": [...],
  "answers": [0, 2, 1, 0, 3]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "score": 4,
    "total_questions": 5,
    "percentage": 80.0,
    "passed": true,
    "correct_answers": [0, 2, 1, 0, 2],
    "explanations": ["...", "...", "...", "...", "..."],
    "feedback": "Great job! You're doing well. Review the areas you missed and continue practicing to master this skill."
  },
  "message": "Quiz evaluated successfully"
}
```

## Backend Architecture

### Files Created/Modified

1. **`src/handlers/assessment_handler.py`**
   - API endpoints for question generation and evaluation
   - Request/response models
   - Error handling

2. **`src/services/assessment_service.py`**
   - Groq API integration
   - Question generation logic
   - Quiz evaluation logic
   - Personalized feedback generation
   - Fallback templates for offline mode

3. **`src/main.py`**
   - Registered assessment router

### Key Components

**AssessmentService Class:**
- `call_groq()` - Communicates with Groq API
- `generate_questions()` - Creates skill-based questions
- `evaluate_quiz()` - Scores and provides feedback
- `_generate_feedback()` - AI-powered personalized feedback
- `_generate_fallback_questions()` - Template questions when AI unavailable

## Frontend Architecture

### Updated Files

**`frontend/app/skillgenie/assessment/page.tsx`**
- Replaced hardcoded questions with API calls
- Added loading and error states
- Integrated quiz evaluation API
- Enhanced results display with AI feedback
- Added review section for incorrect answers

### User Flow

1. **Start Assessment**
   - User navigates to `/skillgenie/assessment?skill=Python`
   - Frontend calls `/assessment/generate-questions`
   - AI generates 5 questions

2. **Take Quiz**
   - User answers questions one by one
   - Progress tracked visually
   - Answers stored locally

3. **Submit & Evaluate**
   - Frontend calls `/assessment/evaluate-quiz`
   - AI evaluates answers and generates feedback
   - Results displayed with score and explanations

4. **Next Steps**
   - If passed (≥60%): Route to main project
   - If failed (<60%): Route to beginner project

## Configuration

### Environment Variables

**Backend `.env`:**
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
```

### Groq API Settings
- **Model**: Llama 3.1 70B Versatile
- **Temperature**: 0.7 (questions), 0.8 (feedback)
- **Max Tokens**: 2000
- **Response Format**: JSON object
- **Timeout**: 60 seconds

## Features

### Question Generation
✅ Skill-specific questions
✅ Difficulty levels (beginner/intermediate/advanced)
✅ 4 multiple-choice options
✅ Single correct answer
✅ Explanations included
✅ Practical, real-world focused
✅ Fallback templates for offline mode

### Quiz Evaluation
✅ Automatic scoring
✅ Percentage calculation
✅ Pass/fail determination (60% threshold)
✅ AI-generated personalized feedback
✅ Detailed explanations for all questions
✅ Review incorrect answers

### User Experience
✅ Loading states with spinners
✅ Error handling with retry
✅ Progress bar
✅ Interactive UI
✅ Responsive design
✅ Smooth transitions
✅ Clear feedback

## Testing

### Test the Integration

1. **Start Backend**:
   ```bash
   cd backend
   .\venv\Scripts\activate
   python -m uvicorn src.main:app --reload --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Flow**:
   - Login to application
   - Navigate to SkillGenie
   - Select a skill
   - Start assessment
   - Answer questions
   - View AI-generated results

### API Testing

**Generate Questions:**
```bash
curl -X POST http://localhost:8000/assessment/generate-questions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"skill": "Python", "difficulty": "intermediate", "num_questions": 5}'
```

**Evaluate Quiz:**
```bash
curl -X POST http://localhost:8000/assessment/evaluate-quiz \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"skill": "Python", "questions": [...], "answers": [0,1,2,0,1]}'
```

## Benefits

1. **Dynamic Content**: Questions generated on-demand for any skill
2. **Personalized**: AI adapts questions and feedback to skill level
3. **Scalable**: No need to manually create question banks
4. **Intelligent**: AI understands context and provides relevant questions
5. **Fast**: Groq API provides quick response times
6. **Fallback**: Template questions available if API unavailable

## Future Enhancements

- [ ] Question difficulty adaptation based on performance
- [ ] Multi-skill assessments
- [ ] Timed quizzes
- [ ] Question history and analytics
- [ ] Skill proficiency tracking
- [ ] Leaderboards
- [ ] Certificate generation

## Troubleshooting

### Common Issues

**1. "Groq API key not configured"**
- Solution: Add `GROQ_API_KEY` to `backend/.env`

**2. "Failed to generate questions"**
- Solution: Check internet connection and API key validity
- Fallback: System uses template questions automatically

**3. Questions not loading**
- Solution: Check backend logs for errors
- Verify authentication token is valid

**4. Evaluation fails**
- Solution: Ensure questions array matches answers array length
- Check backend logs for detailed error

## Status

✅ **Complete and Ready to Use**

- Backend API endpoints implemented
- Groq API integrated
- Frontend updated with API calls
- Error handling and fallbacks in place
- Testing completed

---

**Integration Date**: March 9, 2026
**API Provider**: Groq (Llama 3.1 70B)
**Status**: Production Ready
