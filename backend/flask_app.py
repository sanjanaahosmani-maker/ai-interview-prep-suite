"""
Flask Backend for AI Interview Prep Suite
Complete interview preparation platform with AI-powered features
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from dotenv import load_dotenv
from functools import wraps
from urllib.parse import urljoin, urlparse
import sys
import os
import uuid
import re
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
from auth import init_db, create_user, verify_user, get_user_by_id

# Initialize Flask app
template_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

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

# Initialize auth database
init_db()


def is_safe_next_url(target):
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get('user_id'):
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            next_url = request.path
            return redirect(url_for('login', next=next_url))
        return view_func(*args, **kwargs)

    return wrapped_view


@app.context_processor
def inject_current_user():
    user = None
    user_id = session.get('user_id')
    if user_id:
        user = get_user_by_id(user_id)
        if not user:
            session.clear()
    return {'current_user': user}

# ========================
# AUTH ROUTES
# ========================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if session.get('user_id'):
        return redirect(url_for('home'))

    next_url = request.args.get('next', '')
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        if not email or not password:
            return render_template('login.html', error='Email and password are required.', email=email), 400

        user = verify_user(email, password)
        if not user:
            return render_template('login.html', error='Invalid email or password.', email=email), 401

        session.clear()
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session.permanent = True

        target = next_url if is_safe_next_url(next_url) else url_for('home')
        return redirect(target)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if session.get('user_id'):
        return redirect(url_for('home'))

    next_url = request.args.get('next', '')
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        confirm_password = request.form.get('confirm_password') or ''

        if not name or not email or not password:
            return render_template('register.html', error='All fields are required.', name=name, email=email), 400

        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            return render_template('register.html', error='Please enter a valid email address.', name=name, email=email), 400

        if len(password) < 8:
            return render_template('register.html', error='Password must be at least 8 characters long.', name=name, email=email), 400

        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match.', name=name, email=email), 400

        created, error = create_user(name, email, password)
        if not created:
            return render_template('register.html', error=error, name=name, email=email), 409

        user = verify_user(email, password)
        session.clear()
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session.permanent = True

        target = next_url if is_safe_next_url(next_url) else url_for('home')
        return redirect(target)

    return render_template('register.html', name='', email='')


@app.route('/logout')
def logout():
    """Logout current user"""
    session.clear()
    return redirect(url_for('login'))


# ========================
# PAGE ROUTES
# ========================

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')


@app.route('/resume-builder')
@login_required
def resume_page():
    """Resume builder page"""
    return render_template('resume_builder.html')


@app.route('/ats')
@login_required
def ats_page():
    """ATS resume analysis page"""
    return render_template('ats.html')


@app.route('/interview-qa')
@login_required
def interview_qa_page():
    """Interview Q&A page"""
    return render_template('interview_qa.html')


@app.route('/study-concepts')
@login_required
def study_concepts_page():
    """Study concepts page"""
    return render_template('study_concepts.html')


@app.route('/mock-interview')
@login_required
def mock_interview_page():
    """Mock interview page"""
    return render_template('mock_interview.html')


# ========================
# API ROUTES - RESUME
# ========================

@app.route('/api/ats/analyze', methods=['POST'])
def analyze_ats():
    """Analyze resume text for ATS readability and keyword alignment."""
    data = request.get_json(silent=True) or {}
    resume_text = (data.get('resume_text') or '').strip()
    job_description = (data.get('job_description') or '').strip()

    if not resume_text:
        return jsonify({'success': False, 'error': 'Resume text is required'}), 400

    stop_words = {
        'and', 'the', 'with', 'for', 'from', 'you', 'your', 'our', 'that', 'this',
        'are', 'will', 'have', 'has', 'was', 'were', 'role', 'work', 'job', 'team'
    }

    def keywords(text):
        words = re.findall(r'[A-Za-z][A-Za-z0-9+#.-]{1,}', text.lower())
        phrases = re.findall(r'[A-Za-z][A-Za-z0-9+#.-]*(?:\s+[A-Za-z][A-Za-z0-9+#.-]*)?', text)
        values = {word for word in words if len(word) >= 3 and word not in stop_words}
        return values

    resume_words = keywords(resume_text)
    job_words = keywords(job_description) if job_description else set()
    matched = sorted(resume_words & job_words)
    missing = sorted(job_words - resume_words)

    if job_words:
        keyword_score = round(len(matched) / len(job_words) * 100)
    else:
        keyword_score = 70

    lower_resume = resume_text.lower()
    section_score = sum(12 for name in ('experience', 'education', 'skills', 'projects')
                         if name in lower_resume)
    contact_score = 12 if re.search(r'[\w.+-]+@[\w.-]+', lower_resume) else 0
    contact_score += 8 if re.search(r'\+?[0-9][0-9 ().-]{7,}[0-9]', resume_text) else 0

    score = min(100, round(keyword_score * 0.55 + section_score + contact_score))

    recommendations = []
    if missing:
        recommendations.append('Add relevant keywords naturally: ' + ', '.join(missing[:8]))
    if 'experience' not in lower_resume:
        recommendations.append('Include a clearly labeled Experience section.')
    if 'education' not in lower_resume:
        recommendations.append('Include a clearly labeled Education section.')
    if 'skills' not in lower_resume:
        recommendations.append('Add a dedicated Skills section.')
    if not re.search(r'[\w.+-]+@[\w.-]+', lower_resume):
        recommendations.append('Add a professional email address.')
    if not recommendations:
        recommendations.append('Your resume structure looks ATS-friendly. Quantify achievements with numbers and outcomes.')

    return jsonify({
        'success': True,
        'score': score,
        'keyword_match': round(len(matched) / len(job_words) * 100) if job_words else None,
        'matched_keywords': matched[:20],
        'missing_keywords': missing[:20],
        'recommendations': recommendations
    }), 200


@app.route('/api/resume/generate', methods=['POST'])
def generate_resume():
    """Generate resume from user profile"""
    try:
        data = request.json
        
        logger.info(f"Resume generation request received with data: {data}")
        
        # Validate required fields
        required_fields = ['name', 'email', 'target_role']
        if not all(data.get(field) for field in required_fields):
            logger.error(f"Missing required fields. Received: {list(data.keys())}")
            return jsonify({
                'success': False,
                'error': 'Missing required fields: name, email, target_role'
            }), 400
        
        profile_dict = {
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'target_role': data.get('target_role', ''),
            'experience': data.get('experience', ''),
            'education': data.get('education', ''),
            'skills': data.get('skills', ''),
            'projects': data.get('projects', ''),
            'certifications': data.get('certifications', '')
        }
        
        logger.info(f"Building resume for: {profile_dict['name']} - {profile_dict['target_role']}")
        
        # Generate resume
        resume = resume_builder.build_resume(profile_dict)
        
        if not resume or resume.startswith("Invalid"):
            logger.error(f"Resume builder returned invalid response: {resume}")
            return jsonify({
                'success': False,
                'error': 'Failed to generate resume'
            }), 500
        
        logger.info(f"Resume generated successfully. Length: {len(resume)} chars")
        
        return jsonify({
            'success': True,
            'resume': resume,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating resume: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f"Error: {str(e)}"
        }), 500


@app.route('/api/resume/optimize', methods=['POST'])
def optimize_resume():
    """Get resume optimization suggestions"""
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        target_role = data.get('target_role', '')
        
        if not resume_text or not target_role:
            return jsonify({
                'success': False,
                'error': 'Missing resume_text or target_role'
            }), 400
        
        suggestions = resume_builder.optimize_resume(resume_text, target_role)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        logger.error(f"Error optimizing resume: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Error optimizing resume: {str(e)}"
        }), 500


# ========================
# API ROUTES - INTERVIEW QUESTIONS
# ========================

@app.route('/api/interview/questions', methods=['POST'])
def get_interview_questions():
    """Generate interview questions for a role"""
    try:
        data = request.json
        role = data.get('role', '')
        experience_level = data.get('experience_level', 'mid')
        domain = data.get('domain', '')
        count = int(data.get('count', 5))
        
        if not role:
            return jsonify({
                'success': False,
                'error': 'Missing role'
            }), 400
        
        # Generate questions
        questions = question_generator.generate_questions(
            role=role,
            experience_level=experience_level,
            domain=domain or role,
            count=count
        )
        
        return jsonify({
            'success': True,
            'questions': questions,
            'count': len(questions)
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Error generating questions: {str(e)}"
        }), 500


@app.route('/api/interview/evaluate', methods=['POST'])
def evaluate_answer():
    """Evaluate user's interview answer"""
    try:
        data = request.json
        question = data.get('question', '')
        user_answer = data.get('user_answer', '')
        ideal_answer = data.get('ideal_answer', '')
        
        if not all([question, user_answer, ideal_answer]):
            return jsonify({
                'success': False,
                'error': 'Missing question, user_answer, or ideal_answer'
            }), 400
        
        feedback = question_generator.get_question_feedback(
            question, user_answer, ideal_answer
        )
        
        return jsonify({
            'success': True,
            'feedback': feedback
        }), 200
        
    except Exception as e:
        logger.error(f"Error evaluating answer: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Error evaluating answer: {str(e)}"
        }), 500


# ========================
# API ROUTES - STUDY CONCEPTS
# ========================

@app.route('/api/study/concepts', methods=['POST'])
def get_study_concepts():
    """Get study concepts for a role"""
    try:
        data = request.json
        role = data.get('role', '')
        experience_level = data.get('experience_level', 'intermediate')
        
        if not role:
            return jsonify({
                'success': False,
                'error': 'Missing role'
            }), 400
        
        concepts = study_curator.get_study_path(role, experience_level)
        
        return jsonify({
            'success': True,
            'concepts': concepts,
            'role': role,
            'level': experience_level
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting study concepts: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Error getting study concepts: {str(e)}"
        }), 500


@app.route('/api/study/topic/<topic>', methods=['GET'])
def get_topic_details(topic):
    """Get detailed information about a specific topic"""
    try:
        role = request.args.get('role', 'General')
        details = study_curator.get_topic_details(topic, role)
        
        return jsonify({
            'success': True,
            'topic_details': details
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting topic details: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Error getting topic details: {str(e)}"
        }), 500


# ========================
# API ROUTES - MOCK INTERVIEW
# ========================

@app.route('/api/mock-interview/start', methods=['POST'])
def start_mock_interview():
    """Start a mock interview session"""
    try:
        data = request.json
        role = data.get('role', '')
        experience_level = data.get('experience_level', 'mid')
        domain = data.get('domain', '')
        num_questions = int(data.get('num_questions', 5))
        
        if not role:
            return jsonify({
                'success': False,
                'error': 'Missing role'
            }), 400
        
        # Generate questions for the session
        questions = question_generator.generate_questions(
            role=role,
            experience_level=experience_level,
            domain=domain or role,
            count=num_questions
        )
        
        # Create session
        session_id = str(uuid.uuid4())
        mock_sessions[session_id] = {
            'role': role,
            'experience_level': experience_level,
            'domain': domain,
            'questions': questions,
            'current_question_index': 0,
            'responses': [],
            'scores': [],
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        current_question = questions[0] if questions else None
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total_questions': len(questions),
            'current_question': current_question,
            'current_question_index': 0
        }), 200
        
    except Exception as e:
        logger.error(f"Error starting mock interview: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Error starting mock interview: {str(e)}"
        }), 500


@app.route('/api/mock-interview/<session_id>/next', methods=['POST'])
def next_question(session_id):
    """Get next question in mock interview"""
    try:
        if session_id not in mock_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid session ID'
            }), 404
        
        data = request.json
        user_response = data.get('response', '')
        
        session_data = mock_sessions[session_id]
        questions = session_data['questions']
        current_index = session_data['current_question_index']
        
        # Store response if provided
        if user_response and current_index < len(questions):
            session_data['responses'].append(user_response)
            
            # Get feedback for the response
            current_q = questions[current_index]
            feedback = question_generator.get_question_feedback(
                current_q.get('question', ''),
                user_response,
                current_q.get('ideal_answer', '')
            )
            session_data['scores'].append(feedback)
        
        # Move to next question
        session_data['current_question_index'] += 1
        next_index = session_data['current_question_index']
        
        if next_index >= len(questions):
            # Interview completed
            return jsonify({
                'success': True,
                'completed': True,
                'total_questions': len(questions),
                'session_id': session_id
            }), 200
        
        next_q = questions[next_index]
        
        return jsonify({
            'success': True,
            'current_question': next_q,
            'current_question_index': next_index,
            'total_questions': len(questions),
            'previous_feedback': session_data['scores'][-1] if session_data['scores'] else None
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting next question: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Error getting next question: {str(e)}"
        }), 500


@app.route('/api/mock-interview/<session_id>/complete', methods=['POST'])
def complete_mock_interview(session_id):
    """Complete mock interview and get summary"""
    try:
        if session_id not in mock_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid session ID'
            }), 404
        
        session_data = mock_sessions[session_id]
        session_data['status'] = 'completed'
        session_data['completed_at'] = datetime.now().isoformat()
        
        # Calculate overall score
        if session_data['scores']:
            total_score = sum([s.get('score', 0) for s in session_data['scores']])
            average_score = total_score / len(session_data['scores']) if session_data['scores'] else 0
        else:
            average_score = 0
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'role': session_data['role'],
            'experience_level': session_data['experience_level'],
            'total_questions': len(session_data['questions']),
            'responses_count': len(session_data['responses']),
            'average_score': average_score,
            'feedback': session_data['scores'],
            'created_at': session_data['created_at'],
            'completed_at': session_data['completed_at']
        }), 200
        
    except Exception as e:
        logger.error(f"Error completing mock interview: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Error completing mock interview: {str(e)}"
        }), 500


# ========================
# UTILITY ROUTES
# ========================

@app.route('/api/roles', methods=['GET'])
def get_roles():
    """Get available job roles"""
    roles = [
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Data Scientist",
        "Data Analyst",
        "DevOps Engineer",
        "Cloud Architect",
        "Machine Learning Engineer",
        "Product Manager",
        "UI/UX Designer",
        "QA Engineer",
        "Security Engineer"
    ]
    return jsonify({'success': True, 'roles': roles}), 200


@app.route('/api/experience-levels', methods=['GET'])
def get_experience_levels():
    """Get available experience levels"""
    levels = ["junior", "mid", "senior"]
    return jsonify({'success': True, 'levels': levels}), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'AI Interview Prep Suite',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200


# ========================
# ERROR HANDLERS
# ========================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'status': 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'status': 500
    }), 500


# ========================
# MAIN ENTRY POINT
# ========================

if __name__ == '__main__':
    # Get configuration
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    
    logger.info(f"Starting AI Interview Prep Suite on {host}:{port}")
    logger.info(f"Debug mode: {debug_mode}")
    
    app.run(host=host, port=port, debug=debug_mode)
