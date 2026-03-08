@echo off
echo ========================================
echo Eligify Project Setup (Windows)
echo ========================================
echo.

REM Check Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+ from python.org
    exit /b 1
)
echo Python found!
echo.

REM Check Node.js
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 18+ from nodejs.org
    exit /b 1
)
echo Node.js found!
echo.

REM Backend Setup
echo [3/6] Setting up backend...
cd backend
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing Python dependencies...
pip install -r requirements.txt
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo IMPORTANT: Please edit backend\.env with your configuration!
)
cd ..
echo Backend setup complete!
echo.

REM Frontend Setup
echo [4/6] Setting up frontend...
cd frontend
if not exist node_modules (
    echo Installing Node.js dependencies...
    call npm install
) else (
    echo Node modules already installed, skipping...
)
cd ..
echo Frontend setup complete!
echo.

REM Data directories
echo [5/6] Checking data directories...
if not exist backend\data\persistence (
    mkdir backend\data\persistence
    echo Created persistence directory
)
echo.

echo [6/6] Setup Summary
echo ========================================
echo Backend: eligify-ai-for-bharat\backend
echo Frontend: eligify-ai-for-bharat\frontend
echo.
echo NEXT STEPS:
echo 1. Edit backend\.env with your configuration
echo 2. Optional: Install Ollama for AI features
echo    - Download from: https://ollama.com/download
echo    - Run: ollama pull llama3.1:8b
echo.
echo TO START THE PROJECT:
echo Backend:  cd backend ^&^& venv\Scripts\activate ^&^& python quick_start.py
echo Frontend: cd frontend ^&^& npm run dev
echo.
echo ========================================
echo Setup complete! Happy coding!
echo ========================================
pause
