@echo off
REM Setup script for AI Interview Prep Suite (Windows)

setlocal enabledelayedexpansion

echo 🚀 AI Interview Prep Suite - Setup
echo ====================================
echo.

REM Check Python version
echo 📋 Checking Python version...
python --version
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Setup environment file
echo ⚙️  Setting up environment...
if not exist ".env" (
    copy .env.example .env
    echo ✓ Created .env file from template
    echo.
    echo ⚠️  IMPORTANT: Edit .env and add your API keys:
    echo    - GROQ_API_KEY ^(recommended^) or GEMINI_API_KEY
    echo    - SECRET_KEY ^(for Flask sessions^)
) else (
    echo ✓ .env file already exists
)
echo.

echo ✨ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Edit .env file and add your LLM API key
echo 2. Run: python backend\flask_app.py  (from cmd or PowerShell)
echo 3. Open http://localhost:5000 in your browser
echo.
pause
    echo ✅ Created .env file from template
    echo ⚠️  Please edit .env and add your API keys
    echo    - Groq: https://groq.com
    echo    - Google Gemini: https://aistudio.google.com
) else (
    echo ✅ .env file already exists
)

echo.
echo 🎉 Setup complete!
echo.
echo To run the application:
echo.
echo 1. Activate virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Start Streamlit app:
echo    streamlit run frontend\app.py
echo.
echo 3. Open browser to: http://localhost:8501
echo.
echo Optional: Run FastAPI backend
echo    cd backend
echo    python -m uvicorn main:app --reload
echo.
pause
