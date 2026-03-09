@echo off
echo ============================================
echo Checking Backend Server Status
echo ============================================
echo.

echo Checking if backend is running on port 8000...
curl -s http://localhost:8000/health >nul 2>&1

if %errorlevel% equ 0 (
    echo [SUCCESS] Backend server is running!
    echo.
    curl http://localhost:8000/health
) else (
    echo [ERROR] Backend server is NOT running!
    echo.
    echo Please start the backend server:
    echo   cd backend
    echo   python -m uvicorn src.main:app --reload
)

echo.
echo ============================================
pause
