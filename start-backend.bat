@echo off
echo ========================================
echo Starting Eligify Backend Server
echo ========================================
echo.

cd backend
call venv\Scripts\activate.bat
echo Backend server starting on http://localhost:8000
echo API Docs available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn src.main:app --reload --port 8000
