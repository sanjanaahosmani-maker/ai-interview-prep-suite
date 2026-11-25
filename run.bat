@echo off
REM Quick run script for AI Interview Prep Suite (Windows)
REM This script activates the virtual environment and starts Flask

echo.
echo 🚀 Starting AI Interview Prep Suite...
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found
    echo Copying from .env.example...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env and add your API key:
    echo    - GROQ_API_KEY or GEMINI_API_KEY
    echo.
)

REM Start Flask server
echo.
echo 🌐 Starting Flask server...
echo ===============================
echo.
echo 📍 Server will be available at: http://localhost:3000
echo.
echo Press CTRL+C to stop the server
echo.

python backend\flask_app.py

if errorlevel 1 (
    echo.
    echo ❌ Error starting server
    pause
)
