#!/bin/bash
# Setup script for AI Interview Prep Suite (Unix/Linux/Mac)

set -e

echo "🚀 AI Interview Prep Suite - Setup"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python --version 2>&1 || python3 --version)
echo "✓ Found: $python_version"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if command -v python3 &> /dev/null; then
    python3 -m venv venv
else
    python -m venv venv
fi
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt
echo "✓ Dependencies installed"
echo ""

# Setup environment file
echo "⚙️  Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys:"
    echo "   - GROQ_API_KEY (recommended) or GEMINI_API_KEY"
    echo "   - SECRET_KEY (for Flask sessions)"
else
    echo "✓ .env file already exists"
fi
echo ""

echo "✨ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file and add your LLM API key"
echo "2. Run: source venv/bin/activate  # Activate virtual environment"
echo "3. Run: python backend/flask_app.py  # Start the Flask server"
echo "4. Open http://localhost:5000 in your browser"
echo ""

# Configure environment
echo ""
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "⚠️  Please edit .env and add your API keys"
    echo "   - Groq: https://groq.com"
    echo "   - Google Gemini: https://aistudio.google.com"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo ""
echo "1. Activate virtual environment:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   venv\\Scripts\\activate"
else
    echo "   source venv/bin/activate"
fi
echo ""
echo "2. Start Streamlit app:"
echo "   streamlit run frontend/app.py"
echo ""
echo "3. Open browser to: http://localhost:8501"
echo ""
echo "Optional: Run FastAPI backend"
echo "   cd backend"
echo "   python -m uvicorn main:app --reload"
echo ""
