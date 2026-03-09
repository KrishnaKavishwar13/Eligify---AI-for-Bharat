# Skills Extraction - Groq Integration with Ollama Fallback

## Overview
Skills extraction now uses Groq API as the primary service with automatic fallback to Ollama if Groq fails. This ensures reliable skill extraction from resumes.

## Implementation Details

### Primary: Groq API
- **Model**: `llama-3.3-70b-versatile`
- **Temperature**: 0.2 (for consistent, focused extraction)
- **Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
- **API Key**: Configured in `.env` as `GROQ_API_KEY`

### Fallback: Ollama
- **Model**: `llama3.1:8b`
- **Temperature**: 0.2
- **Endpoint**: `http://localhost:11434/api/generate`
- **Requirement**: Ollama must be running locally (`ollama serve`)

## How It Works

1. **Groq Attempt**: System first tries to extract skills using Groq API
   - If successful: Returns extracted skills immediately
   - If fails: Logs warning and falls back to Ollama

2. **Ollama Fallback**: If Groq fails, system attempts Ollama
   - If successful: Returns extracted skills
   - If fails: Returns empty skills array

3. **Error Handling**: Both services have robust error handling
   - JSON parsing errors
   - Connection timeouts
   - Empty responses
   - Invalid skill formats

## Skill Extraction Format

The AI extracts skills in the following format:

```json
{
  "skills": [
    {
      "name": "Python",
      "category": "programming_language",
      "proficiency": 90
    },
    {
      "name": "React",
      "category": "framework",
      "proficiency": 85
    }
  ]
}
```

### Categories
- `programming_language`: Python, Java, JavaScript, C++, etc.
- `framework`: React, Django, Spring, Angular, etc.
- `tool`: Git, Docker, AWS, Jenkins, etc.
- `soft_skill`: Communication, Leadership, Teamwork, etc.
- `domain_knowledge`: Machine Learning, Data Analysis, etc.
- `database`: PostgreSQL, MongoDB, Redis, etc.

### Proficiency Levels
- **80-100**: Expert level (2+ years, advanced projects)
- **60-79**: Intermediate level (1-2 years, moderate experience)
- **40-59**: Beginner level (< 1 year, basic knowledge)

## Testing

### Test Results
```
✅ Successfully extracted 20 skills from sample resume
✅ Proper categorization (programming_language, framework, tool, soft_skill, database)
✅ Accurate proficiency estimation based on experience level
✅ Groq API working as primary service
✅ Fallback mechanism ready for Ollama
```

### Test Command
```bash
cd backend
python test_skills_extraction.py
```

## Configuration

### Environment Variables (.env)
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Settings (src/config/settings.py)
```python
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
```

## Usage Flow

1. **User uploads resume** on Dashboard or Profile tab
2. **Backend extracts text** from PDF/DOCX file
3. **AI Service processes text**:
   - Attempts Groq API extraction
   - Falls back to Ollama if needed
4. **Skills are validated** and stored in user profile
5. **Frontend displays** extracted skills with categories

## Advantages of Groq Primary

1. **No Local Setup**: No need to run Ollama locally
2. **Faster Response**: Cloud-based API is typically faster
3. **Better Model**: llama-3.3-70b is more capable than llama3.1:8b
4. **Reliability**: Professional API with high uptime
5. **Fallback Safety**: Ollama available if Groq has issues

## Files Modified

- `backend/src/services/ai_service.py`: Added Groq-first logic with Ollama fallback
- `backend/test_skills_extraction.py`: Test script for verification

## Current AI Service Usage

| Feature | Primary Service | Fallback |
|---------|----------------|----------|
| Skills Extraction | Groq API | Ollama |
| Project Generation | Groq API | Template-based |
| QA Module | Groq API | Template-based |

## Logs

The system logs the extraction process:
```
INFO: Attempting skill extraction with Groq API
INFO: ✅ Groq extracted 20 skills from resume
```

Or if fallback occurs:
```
WARNING: Groq skill extraction failed: [error], falling back to Ollama
INFO: Falling back to Ollama for skill extraction
INFO: ✅ Ollama extracted 18 skills from resume
```

## Next Steps

To test the complete flow:
1. Start backend: `cd backend && python -m uvicorn src.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Login to application
4. Upload a resume on Dashboard or Profile tab
5. Verify skills are extracted and displayed correctly

---

**Status**: ✅ Complete and Tested
**Date**: March 9, 2026
