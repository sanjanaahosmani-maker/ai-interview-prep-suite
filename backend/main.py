"""
Flask Backend for AI Interview Prep Suite
Complete interview preparation platform with AI-powered features
"""

from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import sys
import os
import json
from datetime import datetime, timedelta
import logging

# Load environment variables
load_dotenv()

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

from llm_service import LLMService
from resume_builder import ResumeBuilder
from question_generator import QuestionGenerator
from study_concepts import StudyConceptsCurator

# Initialize Flask app
app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static')
)

# Configure app
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Enable CORS
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
llm_service = LLMService()
resume_builder = ResumeBuilder()
question_generator = QuestionGenerator()
study_curator = StudyConceptsCurator()

# Store active mock interview sessions
mock_sessions = {}


class InterviewParams(BaseModel):
    """Parameters for interview question generation"""
    role: str
    experience_level: str
    domain: str
    count: int = 5


class AnswerFeedback(BaseModel):
    """Request for answer evaluation"""
    question: str
    user_answer: str
    ideal_answer: str


class MockInterviewStart(BaseModel):
    """Start mock interview session"""
    role: str
    experience_level: str
    domain: str
    num_questions: int = 5


# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Interview Prep Suite API",
        "version": "1.0.0"
    }


# Resume Endpoints
@app.post("/api/resume/generate")
async def generate_resume(profile: UserProfile):
    """Generate resume from user profile"""
    try:
        builder = ResumeBuilder()
        profile_dict = profile.dict()
        resume = builder.build_resume(profile_dict)
        return {
            "success": True,
            "resume": resume,
            "profile": profile_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")


@app.post("/api/resume/optimize")
async def optimize_resume(resume_text: str, target_role: str):
    """Get resume optimization suggestions"""
    try:
        builder = ResumeBuilder()
        suggestions = builder.optimize_resume(resume_text, target_role)
        return {
            "success": True,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing resume: {str(e)}")


# Interview Question Endpoints
@app.post("/api/interview/questions")
async def generate_questions(params: InterviewParams):
    """Generate interview questions"""
    try:
        gen = QuestionGenerator()
        questions = gen.generate_questions(
            params.role,
            params.experience_level,
            params.domain,
            params.count
        )
        return {
            "success": True,
            "questions": questions,
            "count": len(questions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@app.post("/api/interview/evaluate")
async def evaluate_answer(feedback: AnswerFeedback):
    """Evaluate a mock interview answer"""
    try:
        gen = QuestionGenerator()
        evaluation = gen.get_question_feedback(
            feedback.question,
            feedback.user_answer,
            feedback.ideal_answer
        )
        return {
            "success": True,
            "evaluation": evaluation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating answer: {str(e)}")


# Study Concepts Endpoints
@app.get("/api/study/{role}/{level}")
async def get_study_path(role: str, level: str):
    """Get study path for a role"""
    try:
        curator = StudyConceptsCurator()
        concepts = curator.get_study_path(role, level)
        return {
            "success": True,
            "role": role,
            "level": level,
            "concepts": concepts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting study path: {str(e)}")


@app.get("/api/study/topic/{topic}")
async def get_topic_details(topic: str, role: str = "General"):
    """Get detailed information about a topic"""
    try:
        curator = StudyConceptsCurator()
        details = curator.get_topic_details(topic, role)
        return {
            "success": True,
            "topic_details": details
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting topic details: {str(e)}")


# Mock Interview Endpoints
@app.post("/api/mock-interview/start")
async def start_mock_interview(params: MockInterviewStart):
    """Start a mock interview session"""
    try:
        simulator = MockInterviewSimulator()
        session_info = simulator.start_interview(
            params.role,
            params.experience_level,
            params.domain,
            params.num_questions
        )
        return {
            "success": True,
            "session_info": session_info,
            "session_id": hash(str(simulator.current_session))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting interview: {str(e)}")


@app.post("/api/mock-interview/submit")
async def submit_mock_interview_answer(answer: str):
    """Submit answer for mock interview"""
    try:
        # This would need session management in production
        return {
            "success": True,
            "message": "Answer submitted. Session management needed in production."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting answer: {str(e)}")


# LLM Service Endpoints
@app.get("/api/llm/health")
async def check_llm_service():
    """Check LLM service status"""
    try:
        llm = LLMService()
        return {
            "success": True,
            "llm_initialized": llm.client is not None,
            "provider": "Groq" if llm.use_groq else "Gemini"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking LLM: {str(e)}")


# Info Endpoints
@app.get("/api/info/roles")
async def get_supported_roles():
    """Get list of supported job roles"""
    roles = [
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Data Analyst",
        "Data Scientist",
        "Product Manager",
        "DevOps Engineer",
        "Mobile Developer"
    ]
    return {"success": True, "roles": roles}


@app.get("/api/info/domains")
async def get_supported_domains():
    """Get list of supported domains"""
    domains = [
        "Web Development",
        "Mobile Development",
        "Data Science",
        "Machine Learning",
        "DevOps",
        "Cloud Computing",
        "Business Intelligence",
        "Software Architecture"
    ]
    return {"success": True, "domains": domains}


# Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "success": False,
        "error": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
