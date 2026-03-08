@echo off
echo ========================================
echo Eligify Backend - Quick Start
echo ========================================
echo.
echo This script will:
echo   1. Install Python dependencies
echo   2. Create .env file
echo   3. Start the server
echo.
echo This will take 1-2 minutes...
echo.
pause

echo.
echo Step 1: Installing dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo.
    echo Possible solutions:
    echo   1. Make sure Python is installed: python --version
    echo   2. Try: pip install -r requirements.txt --force-reinstall
    echo   3. Or use: quick_start.bat (creates virtual environment)
    echo.
    pause
    exit /b 1
)

echo.
echo Step 2: Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created!
) else (
    echo .env file already exists.
)

echo.
echo ========================================
echo SUCCESS! Ready to start server.
echo ========================================
echo.
echo Starting server on http://127.0.0.1:8000
echo.
echo After server starts, open your browser to:
echo   http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

uvicorn src.main:app --reload

pause
