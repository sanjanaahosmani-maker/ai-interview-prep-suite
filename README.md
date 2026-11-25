# AI Interview Prep Suite (AIPS)

## 🎯 Overview
AI Interview Prep Suite is a comprehensive, AI-powered platform for interview preparation. It helps students and professionals prepare for job interviews through personalized resume building, interview Q&A practice, structured study materials, and mock interview simulations.

**Built with Flask & AI** - Fast, scalable, open-source interview prep platform

## ✨ Features

### Must-Have Features (MVP) ✅
- ✅ **Resume Builder** - Generate ATS-friendly resumes tailored to target roles
- ✅ **Interview Q&A Generator** - AI-generated role-specific questions with ideal answers
- ✅ **Study Concepts** - Structured learning paths organized by difficulty
- ✅ **Mock Interview Simulator** - Realistic interview practice with feedback
- ✅ **Flask Web Application** - Modern web interface with responsive design
- ✅ **REST API** - Complete API for all features

### Nice-to-Have Features (Roadmap)
- ⏳ Voice-based mock interview
- ⏳ Skill gap analysis and personalized study plan
- ⏳ Performance analytics dashboard
- ⏳ PDF export functionality
- ⏳ Multi-language support
- ⏳ User accounts and progress tracking

## 🛠️ Tech Stack

### Frontend
- **HTML5 / CSS3** - Modern responsive design
- **Bootstrap 5** - UI framework for fast development
- **JavaScript (Vanilla)** - Interactive features without frameworks
- **Flask Templates** - Server-side rendering with Jinja2

### Backend
- **Flask 3.0** - Lightweight Python web framework
- **Flask-CORS** - Cross-origin resource sharing support
- **Python 3.8+** - Core application logic
- **Pydantic** - Data validation (legacy)

### LLM Integration
- **Groq API** - Fast inference with open-source models (Recommended)
- **Google Gemini API** - Alternative LLM provider

### Database & Storage
- **In-Memory Sessions** - For mock interview state management
- **JSON** - For data serialization

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- A free API key from either:
  - **Groq** (recommended): https://groq.com
  - **Google Gemini**: https://aistudio.google.com

### Quick Setup (Windows)
```bash
# 1. Clone/download the project
cd ai-interview-prep-suite

# 2. Run setup script
setup.bat

# 3. Edit .env with your API key
# Edit the file and add: GROQ_API_KEY=your_key_here

# 4. Run the server
run.bat
```

### Quick Setup (Mac/Linux)
```bash
# 1. Clone/download the project
cd ai-interview-prep-suite

# 2. Make scripts executable and run setup
chmod +x setup.sh run.sh
./setup.sh

# 3. Edit .env with your API key
nano .env  # Add: GROQ_API_KEY=your_key_here

# 4. Run the server
./run.sh
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API key

# Start Flask server
python backend/flask_app.py
```

The application will be available at: **http://localhost:5000**

## 🚀 Quick Start

### 1. Resume Builder
Navigate to `/resume-builder` and:
- Enter your profile information (education, experience, skills, projects)
- Select target job role
- Click "Generate Resume"
- Review AI-powered optimization suggestions
- Download resume as text file

### 2. Study Concepts
Navigate to `/study-concepts` and:
- Select your target role and experience level
- Browse structured learning path organized by difficulty
- Click on topics to view detailed information including:
  - Key concepts and points
  - Example problems
  - Common mistakes
  - Resources

### 3. Interview Q&A Practice
Navigate to `/interview-qa` and:
- Select role, experience level, and domain
- Generate interview questions
- Click on questions to practice
- View AI-generated ideal answers
- Submit your answer to receive:
  - Score out of 100
  - Strengths in your answer
  - Areas to improve
  - Detailed feedback

### 4. Mock Interview
Navigate to `/mock-interview` and:
- Configure interview (role, experience, # of questions)
- Start the interview session
- Answer questions one by one
- Get immediate feedback on each answer
- View final report with:
  - Average score
  - Performance metrics
  - Detailed feedback per question
  - Downloadable report

## 📊 Project Structure

```
ai-interview-prep-suite/
│
├── backend/
│   ├── flask_app.py              # ⭐ Main Flask application
│   ├── main.py                   # FastAPI (legacy)
│   ├── llm_service.py            # LLM API integration
│   ├── resume_builder.py         # Resume generation
│   ├── question_generator.py     # Interview questions
│   ├── study_concepts.py         # Study material curation
│   └── requirements.txt          # Python dependencies
│
├── frontend/
│   ├── templates/                # HTML templates
│   │   ├── base.html             # Base layout
│   │   ├── index.html            # Home page
│   │   ├── resume_builder.html   # Resume builder
│   │   ├── interview_qa.html     # Interview Q&A
│   │   ├── study_concepts.html   # Study concepts
│   │   └── mock_interview.html   # Mock interview
│   │
│   └── static/
│       ├── css/
│       │   └── style.css         # Main stylesheet
│       └── js/
│           ├── common.js         # Shared utilities
│           ├── home.js           # Home page logic
│           ├── resume_builder.js # Resume builder logic
│           ├── interview_qa.js   # Q&A logic
│           ├── study_concepts.js # Study concepts logic
│           └── mock_interview.js # Mock interview logic
│
├── data/
│   └── sample_data.py            # Fallback data
│
├── .env.example                  # Environment template
├── setup.bat / setup.sh          # Setup scripts
├── run.bat / run.sh              # Run scripts
├── test_api.py                   # API test suite
├── QUICKSTART.md                 # 5-minute quick start
└── README.md                     # This file
```

## 🔑 API Configuration

### Option 1: Groq API (Recommended)
1. Visit https://groq.com
2. Sign up for a free account
3. Generate an API key
4. Add to `.env`: `GROQ_API_KEY=gsk_...`

### Option 2: Google Gemini API
1. Visit https://aistudio.google.com
2. Click "Get API Key"
3. Create new API key
4. Add to `.env`: `GEMINI_API_KEY=AIzaSy...`

## 🧪 Testing the Application

### Test API Endpoints
```bash
pip install requests  # If not already installed
python test_api.py
```

This will test all major API endpoints and verify your setup.

### Manual API Testing
```bash
# Test health check
curl http://localhost:5000/api/health

# Test resume generation
curl -X POST http://localhost:5000/api/resume/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","target_role":"Developer","skills":"Python"}'
```

## 📚 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/roles` | Get available roles |
| GET | `/api/experience-levels` | Get experience levels |

### Resume Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resume/generate` | Generate resume |
| POST | `/api/resume/optimize` | Get optimization suggestions |

### Interview Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/interview/questions` | Generate questions |
| POST | `/api/interview/evaluate` | Evaluate answer |

### Study Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/study/concepts` | Get study concepts |
| GET | `/api/study/topic/<topic>` | Get topic details |

### Mock Interview Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/mock-interview/start` | Start interview |
| POST | `/api/mock-interview/<id>/next` | Get next question |
| POST | `/api/mock-interview/<id>/complete` | Complete interview |

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in .env
PORT=5001

# Or kill the process using port 5000
# Windows: netstat -ano | findstr :5000
# Mac/Linux: lsof -i :5000
```

### API Key Not Working
1. Verify API key is valid in .env
2. Check API provider credentials
3. Restart Flask server after changing .env

### Dependencies Installation Failed
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then install requirements again
pip install -r backend/requirements.txt
```

### Templates Not Loading
Make sure you're running from the project root directory:
```bash
cd /path/to/ai-interview-prep-suite
python backend/flask_app.py
```

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Business context
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment instructions
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - All docs

## 🎓 Tips for Best Results

1. **Detailed Profiles**: Provide comprehensive information for better resume generation
2. **Specific Domains**: Specify domain/industry for more targeted questions
3. **Consistent Practice**: Regular mock interviews improve performance
4. **Review Feedback**: Study the feedback to identify weak areas
5. **Track Progress**: Compare scores across multiple interview sessions

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the project
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open-source and available for educational and commercial use.

## 🎯 Roadmap

- [ ] User authentication system
- [ ] Progress tracking dashboard
- [ ] PDF resume export
- [ ] Voice-based interviews
- [ ] Skill gap analysis
- [ ] Mobile app version
- [ ] Multi-language support

## 💡 Support

For issues, questions, or suggestions:
1. Check [QUICKSTART.md](QUICKSTART.md) for quick fixes
2. Run `python test_api.py` to diagnose issues
3. Review API endpoints documentation above

## 🚀 Get Started Now!

```bash
# Windows
setup.bat && run.bat

# Mac/Linux
chmod +x setup.sh run.sh && ./setup.sh && ./run.sh
```

Then open http://localhost:5000 in your browser!

---

**Happy Interviewing! 🎉**

*AI Interview Prep Suite - Empowering careers through AI-driven preparation*
3. Get API key from dashboard
4. Add to `.env` file: `GROQ_API_KEY=your_key`
5. Supports fast inference with LLaMA, Mistral models

### Google Gemini API (Alternative)
1. Visit [aistudio.google.com](https://aistudio.google.com)
2. Create API key
3. Add to `.env` file: `GEMINI_API_KEY=your_key`
4. Generous free tier available

## 💻 Local Development

### Run Streamlit app
```bash
cd frontend
streamlit run app.py
```

### Run backend API (FastAPI - optional)
```bash
cd backend
python -m uvicorn main:app --reload
```

### Development Server
```bash
# Terminal 1: Streamlit
streamlit run frontend/app.py

# Terminal 2: Backend API (optional)
uvicorn backend.main:app --reload
```

## 🧪 Testing

Run sample code snippets:
```python
from backend.llm_service import LLMService
from backend.resume_builder import ResumeBuilder

# Test LLM Service
llm = LLMService()

# Test Resume Builder
builder = ResumeBuilder()
profile = {
    "name": "John Doe",
    "email": "john@example.com",
    "target_role": "Frontend Developer",
    "experience": "2 years",
    "education": "B.Tech Computer Science",
    "skills": "React, JavaScript, Python"
}
resume = builder.build_resume(profile)
print(resume)
```

## 🎯 Use Cases

### Use Case 1: Student Preparing for Placement
- Use resume builder to create initial resume
- Study concepts relevant to target company
- Practice interview Q&A repeatedly
- Take mock interviews to assess readiness

### Use Case 2: Professional Career Switch
- Rebuild resume for new domain
- Study new role-specific concepts
- Practice with intermediate/senior level questions
- Assess skill gaps

### Use Case 3: Technical Interview Prep
- Focus on technical Q&A practice
- Use study concepts for deep dives
- Take mock interviews for realistic practice
- Review feedback and iterate

## 📈 Performance Optimization

- **Groq API**: Recommended for fastest response times
- **Caching**: Store generated questions and concepts
- **Batch Processing**: Handle multiple users efficiently
- **Async Operations**: Non-blocking LLM calls

## 🚀 Deployment

### Streamlit Cloud (Easiest)
```bash
# Push to GitHub
git push origin main

# Deploy on Streamlit Cloud
# 1. Visit share.streamlit.io
# 2. Connect GitHub repo
# 3. Select app.py as main file
```

### Render.com (Backend)
```bash
# Deploy FastAPI backend
# 1. Create account on render.com
# 2. Create new Web Service
# 3. Connect GitHub repo
# 4. Set build command: pip install -r requirements.txt
# 5. Set start command: uvicorn backend.main:app
```

### Local/Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py"]
```

## 📝 Example API Responses

### Resume Generation
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-XXX-XXX-XXXX",
  "summary": "...",
  "experience": [...],
  "education": [...],
  "skills": [...],
  "projects": [...]
}
```

### Interview Question
```json
{
  "question": "Explain your approach to debugging a slow website.",
  "ideal_answer": "Start with browser DevTools...",
  "key_points": ["Performance metrics", "Code profiling", "Optimization"],
  "evaluation_criteria": ["Systematic approach", "Technical knowledge"]
}
```

### Mock Interview Feedback
```json
{
  "score": 7,
  "strengths": ["Good structure", "Clear explanation"],
  "weaknesses": ["Lacked specific examples"],
  "feedback": "Great response with good technical understanding...",
  "suggestions": ["Add more concrete examples", "Elaborate on implementation"],
  "coverage": 75
}
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional role templates
- More interview questions
- Better feedback generation
- Voice interface for mock interviews
- Analytics dashboard

## 📄 License

Open source - feel free to use and modify

## ✉️ Support

For issues or questions:
- Check README and documentation
- Review example code
- Check API documentation for Groq/Gemini

## 🎓 Learning Resources

- [Groq API Documentation](https://groq.com/api)
- [Google Gemini API](https://ai.google.dev)
- [Streamlit Documentation](https://docs.streamlit.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [LangChain Documentation](https://python.langchain.com)

## 🏆 Judging Criteria

- **Innovation**: AI-driven personalized preparation
- **Functionality**: All 4 must-have features implemented
- **AI/ML Usage**: Effective use of LLMs for content generation and feedback
- **User Experience**: Intuitive Streamlit interface
- **Completeness**: End-to-end working demo
- **Demo Quality**: Clear demonstration of features

---

**Built for the AI Interview Prep Hackathon**

Good luck with your interview preparation! 🎯
