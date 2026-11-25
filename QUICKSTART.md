# 🚀 Flask Quick Start Guide

## AI Interview Prep Suite - Get Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- An API key from Groq (recommended) or Google Gemini

### Step 1: Get an API Key (2 minutes)

#### Option A: Groq (Recommended - Fast & Free)
1. Go to [groq.com](https://groq.com)
2. Sign up for a free account
3. Generate an API key from the dashboard
4. Copy your API key (starts with `gsk_`)

#### Option B: Google Gemini (Free)
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click "Get API Key"
3. Create a new API key
4. Copy your API key

### Step 2: Setup & Install (2 minutes)

#### Windows Users:
```bash
# Run the setup script
setup.bat

# Follow the prompts and edit .env file with your API key
```

#### Mac/Linux Users:
```bash
# Make the scripts executable
chmod +x setup.sh run.sh

# Run the setup script
./setup.sh

# Follow the prompts and edit .env file with your API key
```

### Step 3: Configure API Key (1 minute)

Edit the `.env` file and add your API key:

```env
# Choose ONE of the following:

# Groq API (Recommended)
GROQ_API_KEY=your_api_key_here

# OR Google Gemini API
GEMINI_API_KEY=your_api_key_here

# Flask Configuration
SECRET_KEY=change-this-to-a-random-string

# Server Settings
HOST=0.0.0.0
PORT=5000
DEBUG=False
```

### Step 4: Start the Server

#### Windows:
```bash
run.bat
```

#### Mac/Linux:
```bash
./run.sh
```

Or manually:
```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Start Flask server
python backend/flask_app.py
```

### Step 5: Access the Application

Open your browser and go to:
```
http://localhost:5000
```

---

## 🎯 Features Quick Tour

### 1. **Resume Builder**
- Click "Resume Builder" in navigation
- Fill in your profile information
- Get AI-powered resume with optimization suggestions
- Download as text file

### 2. **Interview Q&A**
- Select your target role and experience level
- Generate role-specific interview questions
- Practice answering with AI-powered feedback
- View ideal answers and evaluation criteria

### 3. **Study Concepts**
- Choose your target role
- Get structured learning paths organized by difficulty
- Review key topics and concepts
- View resources and key points for each topic

### 4. **Mock Interview**
- Set up a mock interview session
- Answer questions one by one
- Get real-time feedback and scoring
- Download performance report

---

## 🧪 Testing the API

To test the Flask API endpoints:

```bash
# Install requests library
pip install requests

# Run the test script
python test_api.py
```

This will test all API endpoints and show you if everything is working correctly.

---

## 📁 Project Structure

```
ai-interview-prep-suite/
├── backend/
│   ├── flask_app.py              # Main Flask application
│   ├── main.py                   # Legacy (FastAPI)
│   ├── llm_service.py            # LLM integration
│   ├── resume_builder.py         # Resume generation logic
│   ├── question_generator.py     # Interview questions logic
│   ├── study_concepts.py         # Study material logic
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── templates/                # HTML templates
│   │   ├── base.html             # Base template
│   │   ├── index.html            # Home page
│   │   ├── resume_builder.html   # Resume builder page
│   │   ├── interview_qa.html     # Interview Q&A page
│   │   ├── study_concepts.html   # Study concepts page
│   │   └── mock_interview.html   # Mock interview page
│   └── static/
│       ├── css/
│       │   └── style.css         # Main stylesheet
│       └── js/
│           ├── common.js         # Common utilities
│           ├── home.js           # Home page logic
│           ├── resume_builder.js # Resume builder logic
│           ├── interview_qa.js   # Interview Q&A logic
│           ├── study_concepts.js # Study concepts logic
│           └── mock_interview.js # Mock interview logic
├── data/
│   └── sample_data.py            # Sample interview data
├── .env.example                  # Environment template
├── setup.bat                     # Windows setup script
├── setup.sh                      # Mac/Linux setup script
├── run.bat                       # Windows run script
├── run.sh                        # Mac/Linux run script
└── test_api.py                   # API test script
```

---

## 🐛 Troubleshooting

### Problem: "Address already in use"
**Solution:** Port 5000 is already in use. Change the port in `.env`:
```env
PORT=5001
```

### Problem: "API key not configured"
**Solution:** 
1. Make sure `.env` file exists
2. Check that you have added your API key (GROQ_API_KEY or GEMINI_API_KEY)
3. Restart the Flask server

### Problem: "Module not found"
**Solution:** Make sure all dependencies are installed:
```bash
pip install -r backend/requirements.txt
```

### Problem: "Connection refused" when testing API
**Solution:** 
1. Make sure Flask server is running on localhost:5000
2. Check if .env file exists with proper API key
3. Try restarting the server

---

## 📚 API Documentation

### Main Endpoints

#### Health Check
```
GET /api/health
Response: { "status": "healthy", "service": "...", "version": "..." }
```

#### Resume Generation
```
POST /api/resume/generate
Body: {
  "name": "...",
  "email": "...",
  "target_role": "...",
  "skills": "...",
  ...
}
Response: { "success": true, "resume": "..." }
```

#### Interview Questions
```
POST /api/interview/questions
Body: {
  "role": "Frontend Developer",
  "experience_level": "mid",
  "domain": "Web Development",
  "count": 5
}
Response: { "success": true, "questions": [...] }
```

#### Study Concepts
```
POST /api/study/concepts
Body: {
  "role": "Backend Developer",
  "experience_level": "intermediate"
}
Response: { "success": true, "concepts": {...} }
```

#### Mock Interview Start
```
POST /api/mock-interview/start
Body: {
  "role": "Data Scientist",
  "experience_level": "junior",
  "num_questions": 5
}
Response: { "success": true, "session_id": "...", "current_question": {...} }
```

---

## 🎓 Tips for Best Results

1. **Get Better Resumes**: Provide detailed information about your experiences and projects
2. **Better Questions**: Specify the domain to get more relevant questions
3. **Focused Learning**: Choose your exact role and experience level for tailored study paths
4. **Realistic Interviews**: Take mock interviews seriously - they simulate real scenarios
5. **Track Progress**: Download reports after each mock interview to track improvements

---

## 📞 Support & Resources

- **API Providers:**
  - [Groq Documentation](https://groq.com/docs)
  - [Google Gemini API](https://ai.google.dev/)

- **Flask Documentation:**
  - [Flask Official Docs](https://flask.palletsprojects.com/)

- **Project Resources:**
  - See `README.md` for detailed project overview
  - See `PROJECT_OVERVIEW.md` for business context
  - See `DOCUMENTATION_INDEX.md` for all documentation

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] `.env` file created with API key
- [ ] Flask server running on localhost:5000
- [ ] Can access http://localhost:5000 in browser
- [ ] API key is properly configured and tested

---

## 🚀 Next Steps

1. ✅ Complete the setup steps above
2. 🎯 Try the Resume Builder first (easiest to test)
3. 📚 Explore Study Concepts for your target role
4. ❓ Practice with Interview Q&A
5. 🎤 Take a Mock Interview to assess yourself
6. 📊 Track your progress over time

---

**Ready to prepare for your dream job? Let's go! 🚀**

For issues or questions, check the documentation or test with `python test_api.py`
