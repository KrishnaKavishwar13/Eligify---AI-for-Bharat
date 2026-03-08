@echo off
REM Eligify Backend - Quick Start Script (Windows)
REM This script helps you get the backend running locally

echo.
echo ================================
echo Eligify Backend - Quick Start
echo ================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo    Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo    Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo    Dependencies installed
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo    .env file created
    echo    Please edit .env file with your configuration
    echo.
)

REM Start server
echo.
echo ================================
echo Starting FastAPI server...
echo ================================
echo.
echo Server will be available at:
echo    - API: http://localhost:8000
echo    - Docs: http://localhost:8000/docs
echo    - Health: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
