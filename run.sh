#!/bin/bash
# Quick run script for AI Interview Prep Suite (Unix/Linux/Mac)
# This script activates the virtual environment and starts Flask

echo ""
echo "🚀 Starting AI Interview Prep Suite..."
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "Copying from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API key:"
    echo "   - GROQ_API_KEY or GEMINI_API_KEY"
    echo ""
fi

# Start Flask server
echo ""
echo "🌐 Starting Flask server..."
echo "==============================="
echo ""
echo "📍 Server will be available at: http://localhost:3000"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python backend/flask_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error starting server"
fi
