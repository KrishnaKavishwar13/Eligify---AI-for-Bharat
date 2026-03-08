@echo off
echo ================================
echo Eligify Deployment Script
echo ================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

echo [OK] Docker found
echo.

REM Build and start services
echo Building Docker images...
docker-compose build

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Pull Ollama model
echo.
echo Pulling Ollama model (this may take a few minutes)...
docker exec eligify-ollama-1 ollama pull llama3.1:8b

echo.
echo ================================
echo Deployment complete!
echo ================================
echo.
echo Access your application:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Test credentials:
echo   Email:    rudradewatwal@gmail.com
echo   Password: Password@123
echo.
echo View logs:
echo   docker-compose logs -f
echo.
echo Stop services:
echo   docker-compose down
echo.
pause
