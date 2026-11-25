"""
AI Interview Prep Suite - Main Streamlit Application
A comprehensive platform for interview preparation
"""

import streamlit as st
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from llm_service import LLMService
from resume_builder import ResumeBuilder
from question_generator import QuestionGenerator, MockInterviewSimulator
from study_concepts import StudyConceptsCurator

# Configure page
st.set_page_config(
    page_title="AI Interview Prep Suite",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .feature-card {
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        margin: 10px 0;
    }
    .success-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'mock_interview_session' not in st.session_state:
    st.session_state.mock_interview_session = None

# Sidebar Navigation
st.sidebar.markdown("# 🎯 AIPS Navigation")
st.sidebar.markdown("---")

pages = {
    "🏠 Home": "home",
    "📄 Resume Builder": "resume",
    "❓ Interview Q&A": "interview_qa",
    "📚 Study Concepts": "study",
    "🎤 Mock Interview": "mock",
    "ℹ️ About": "about"
}

page_choice = st.sidebar.radio("Select a feature:", list(pages.keys()))
current_page = pages[page_choice]

# API Key Setup
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Configuration")
api_provider = st.sidebar.selectbox(
    "Select LLM Provider:",
    ["Groq (Recommended)", "Google Gemini"]
)

api_key = st.sidebar.text_input(
    "Enter your API Key:",
    type="password",
    help="Your API key is not stored. Set environment variables for security."
)

if api_key:
    if "Groq" in api_provider:
        os.environ["GROQ_API_KEY"] = api_key
    else:
        os.environ["GEMINI_API_KEY"] = api_key
    st.sidebar.success("✅ API Key configured!")

# Main Pages
def render_home():
    st.markdown("""
    <div class="main-header">
        <h1>🎯 AI Interview Prep Suite</h1>
        <h3>Your Complete Interview Preparation Platform</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Welcome to AIPS!")
    st.write("""
    The AI Interview Prep Suite is your one-stop platform for comprehensive interview preparation. 
    Whether you're a student preparing for placements or a professional switching roles, AIPS provides 
    personalized, AI-powered guidance across every aspect of interview readiness.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Resume Builder")
        st.write("""
        - Generate ATS-friendly resumes
        - Get AI-powered optimization suggestions
        - Tailor your resume to specific roles
        - Export as PDF
        """)
        if st.button("Go to Resume Builder →", key="home_resume"):
            st.session_state.current_page = "resume"
            st.rerun()
    
    with col2:
        st.markdown("### ❓ Interview Q&A")
        st.write("""
        - Role-specific interview questions
        - AI-generated model answers
        - Detailed evaluation criteria
        - Practice and get feedback
        """)
        if st.button("Go to Interview Q&A →", key="home_qa"):
            st.session_state.current_page = "interview_qa"
            st.rerun()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 📚 Study Concepts")
        st.write("""
        - Structured learning paths
        - Beginner to Advanced topics
        - Role-specific content
        - Organized by difficulty
        """)
        if st.button("Go to Study Concepts →", key="home_study"):
            st.session_state.current_page = "study"
            st.rerun()
    
    with col4:
        st.markdown("### 🎤 Mock Interview")
        st.write("""
        - Realistic interview simulation
        - Real-time feedback
        - Performance scoring
        - Readiness assessment
        """)
        if st.button("Go to Mock Interview →", key="home_mock"):
            st.session_state.current_page = "mock"
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Start")
    st.info("""
    1. **Set up your API Key** in the sidebar (Groq recommended for speed)
    2. **Build your resume** using our AI-powered builder
    3. **Study concepts** relevant to your target role
    4. **Practice interview Q&A** with feedback
    5. **Take a mock interview** to assess readiness
    """)


def render_resume_builder():
    st.title("📄 Resume Builder")
    st.write("Generate an ATS-friendly resume tailored to your target role.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Your Profile")
        
        name = st.text_input("Full Name *", placeholder="John Doe")
        email = st.text_input("Email *", placeholder="john@example.com")
        phone = st.text_input("Phone Number", placeholder="+1-XXX-XXX-XXXX")
        
        st.markdown("### Target Role")
        target_role = st.selectbox(
            "Select target role *",
            ["Frontend Developer", "Backend Developer", "Full Stack Developer", 
             "Data Analyst", "Data Scientist", "Product Manager", "Other"]
        )
        
        years_exp = st.slider("Years of Experience", 0, 30, 2)
        
        st.markdown("### Education")
        education = st.text_area("Education Background", 
                                placeholder="B.Tech Computer Science from XYZ University, 2022")
    
    with col2:
        st.markdown("### Skills & Experience")
        
        skills = st.text_area("Technical Skills (comma-separated) *",
                             placeholder="Python, JavaScript, React, SQL, Machine Learning")
        
        experience = st.text_area("Work Experience",
                                 placeholder="Worked as Junior Developer at ABC Corp for 1 year...")
        
        projects = st.text_area("Notable Projects",
                               placeholder="Built an e-commerce platform using React and Node.js...")
        
        certifications = st.text_area("Certifications (if any)",
                                     placeholder="AWS Certified Solutions Architect")
    
    if st.button("🚀 Generate Resume", key="generate_resume"):
        if not name or not email or not skills:
            st.warning("⚠️ Please fill in marked required fields (*)")
        else:
            with st.spinner("Generating your resume..."):
                builder = ResumeBuilder()
                profile = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "target_role": target_role,
                    "experience": f"{years_exp} years, {experience}",
                    "education": education,
                    "skills": skills,
                    "projects": projects,
                    "certifications": certifications
                }
                
                resume = builder.build_resume(profile)
                
                st.session_state.user_profile = profile
                st.success("✅ Resume generated successfully!")
                
                st.markdown("### Generated Resume")
                st.markdown(f"""
                ```
                {resume}
                ```
                """)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📥 Download PDF"):
                        st.info("PDF download feature coming soon!")
                with col2:
                    if st.button("✨ Get Optimization Tips"):
                        tips = builder.optimize_resume(resume, target_role)
                        with st.expander("See Optimization Suggestions"):
                            st.markdown("#### Missing Keywords")
                            st.write(tips["keywords"])
                            st.markdown("#### Action Verbs to Use")
                            st.write(tips["action_verbs"])
                            st.markdown("#### Improvement Ideas")
                            for imp in tips["improvements"]:
                                st.write(f"- {imp}")


def render_interview_qa():
    st.title("❓ Interview Q&A Generator")
    st.write("Generate role-specific interview questions and practice with AI feedback.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Interview Parameters")
        role = st.selectbox(
            "Target Role",
            ["Frontend Developer", "Backend Developer", "Full Stack Developer",
             "Data Analyst", "Data Scientist", "Product Manager"]
        )
        
        experience_level = st.radio(
            "Experience Level",
            ["Junior (0-2 years)", "Mid (2-5 years)", "Senior (5+ years)"]
        ).split()[0].lower()
        
        domain = st.text_input("Domain/Industry", "Technology/Software Development")
        num_questions = st.slider("Number of Questions", 3, 10, 5)
    
    with col2:
        st.markdown("### Generate Questions")
        if st.button("🔄 Generate Questions", key="gen_questions"):
            with st.spinner("Generating interview questions..."):
                gen = QuestionGenerator()
                questions = gen.generate_questions(role, experience_level, domain, num_questions)
                st.session_state.interview_questions = questions
                st.success(f"✅ Generated {len(questions)} questions!")
    
    if 'interview_questions' in st.session_state and st.session_state.interview_questions:
        st.markdown("---")
        st.markdown("### Generated Questions")
        
        for i, q_data in enumerate(st.session_state.interview_questions, 1):
            with st.expander(f"Question {i}: {q_data.get('question', 'N/A')[:50]}..."):
                st.markdown(f"**Q:** {q_data.get('question', 'N/A')}")
                st.markdown(f"**Model Answer:**\n{q_data.get('ideal_answer', 'N/A')}")
                
                st.markdown("**Key Points:**")
                for point in q_data.get('key_points', []):
                    st.write(f"- {point}")
                
                st.markdown("**Evaluation Criteria:**")
                for criterion in q_data.get('evaluation_criteria', []):
                    st.write(f"- {criterion}")
                
                st.markdown("---")
                user_answer = st.text_area(
                    f"Your Answer to Question {i}:",
                    key=f"answer_{i}",
                    height=100
                )
                
                if st.button(f"Get Feedback", key=f"feedback_{i}"):
                    with st.spinner("Analyzing your answer..."):
                        gen = QuestionGenerator()
                        feedback = gen.get_question_feedback(
                            q_data['question'],
                            user_answer,
                            q_data['ideal_answer']
                        )
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Score", f"{feedback.get('score', 0)}/10")
                        with col2:
                            st.metric("Coverage", f"{feedback.get('coverage', 0)}%")
                        with col3:
                            st.metric("Quality", "Good" if feedback.get('score', 0) >= 7 else "Needs Work")
                        
                        st.markdown(f"**Feedback:** {feedback.get('feedback', 'N/A')}")
                        
                        st.markdown("**Strengths:**")
                        for strength in feedback.get('strengths', []):
                            st.write(f"✅ {strength}")
                        
                        st.markdown("**Areas to Improve:**")
                        for weakness in feedback.get('weaknesses', []):
                            st.write(f"❌ {weakness}")
                        
                        st.markdown("**Suggestions:**")
                        for suggestion in feedback.get('suggestions', []):
                            st.write(f"💡 {suggestion}")


def render_study_concepts():
    st.title("📚 Study Concepts & Learning Paths")
    st.write("Structured study material organized by difficulty and role.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        role = st.selectbox(
            "Target Role",
            ["Frontend Developer", "Backend Developer", "Data Analyst",
             "Data Scientist", "Full Stack Developer"]
        )
        
        experience_level = st.radio(
            "Your Experience Level",
            ["Beginner", "Intermediate", "Advanced"]
        )
    
    with col2:
        st.info("Select your role and experience level to see a personalized learning path")
    
    if st.button("📖 Load Study Path", key="load_study"):
        with st.spinner("Generating study path..."):
            curator = StudyConceptsCurator()
            concepts = curator.get_study_path(role, experience_level.lower())
            st.session_state.study_path = concepts
            st.success("✅ Study path loaded!")
    
    if 'study_path' in st.session_state:
        concepts = st.session_state.study_path
        
        st.markdown("---")
        st.markdown("### 📚 Your Learning Path")
        
        # Beginner concepts
        if concepts.get('beginner'):
            st.markdown("#### 🟢 Beginner Level")
            for topic in concepts['beginner']:
                with st.expander(f"📖 {topic.get('topic', 'Topic')}"):
                    st.write(f"**Description:** {topic.get('description', 'N/A')}")
                    st.write(f"**Why it matters:** {topic.get('importance', 'N/A')}")
                    
                    st.markdown("**Key Points:**")
                    for point in topic.get('key_points', []):
                        st.write(f"- {point}")
                    
                    st.markdown("**Resources:**")
                    for resource in topic.get('resources', []):
                        st.write(f"- {resource}")
        
        # Intermediate concepts
        if concepts.get('intermediate'):
            st.markdown("#### 🟡 Intermediate Level")
            for topic in concepts['intermediate']:
                with st.expander(f"📖 {topic.get('topic', 'Topic')}"):
                    st.write(f"**Description:** {topic.get('description', 'N/A')}")
                    st.write(f"**Why it matters:** {topic.get('importance', 'N/A')}")
                    
                    st.markdown("**Key Points:**")
                    for point in topic.get('key_points', []):
                        st.write(f"- {point}")
                    
                    st.markdown("**Resources:**")
                    for resource in topic.get('resources', []):
                        st.write(f"- {resource}")
        
        # Advanced concepts
        if concepts.get('advanced'):
            st.markdown("#### 🔴 Advanced Level")
            for topic in concepts['advanced']:
                with st.expander(f"📖 {topic.get('topic', 'Topic')}"):
                    st.write(f"**Description:** {topic.get('description', 'N/A')}")
                    st.write(f"**Why it matters:** {topic.get('importance', 'N/A')}")
                    
                    st.markdown("**Key Points:**")
                    for point in topic.get('key_points', []):
                        st.write(f"- {point}")
                    
                    st.markdown("**Resources:**")
                    for resource in topic.get('resources', []):
                        st.write(f"- {resource}")


def render_mock_interview():
    st.title("🎤 Mock Interview Simulator")
    st.write("Practice a realistic interview with AI asking questions and providing feedback.")
    
    if not st.session_state.mock_interview_session:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Start Interview Setup")
            role = st.selectbox(
                "Target Role",
                ["Frontend Developer", "Backend Developer", "Full Stack Developer",
                 "Data Analyst", "Data Scientist", "Product Manager"]
            )
            
            experience_level = st.radio(
                "Experience Level",
                ["Junior", "Mid", "Senior"]
            ).lower()
            
            domain = st.text_input("Domain", "Technology")
            num_questions = st.slider("Number of Questions", 3, 10, 5)
        
        with col2:
            st.markdown("### Tips for Success")
            st.info("""
            - **Be specific**: Use concrete examples
            - **STAR method**: Situation, Task, Action, Result
            - **Pause to think**: It's okay to take a moment
            - **Be conversational**: Explain your thinking
            - **Ask clarifying questions**: Show engagement
            """)
        
        if st.button("🎯 Start Interview", key="start_interview"):
            with st.spinner("Setting up interview..."):
                simulator = MockInterviewSimulator()
                session_info = simulator.start_interview(role, experience_level, domain, num_questions)
                st.session_state.mock_interview_session = simulator.current_session
                st.session_state.current_question_num = 1
                st.rerun()
    
    else:
        # Interview in progress
        session = st.session_state.mock_interview_session
        q_idx = session["current_index"]
        
        if q_idx < len(session["questions"]):
            question = session["questions"][q_idx]
            
            st.progress(q_idx / len(session["questions"]))
            st.markdown(f"### Question {q_idx + 1}/{len(session['questions'])}")
            
            st.markdown(f"**{question['question']}**")
            
            user_answer = st.text_area(
                "Your Answer:",
                height=150,
                key=f"mock_answer_{q_idx}"
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📤 Submit Answer"):
                    if not user_answer.strip():
                        st.warning("Please provide an answer before submitting.")
                    else:
                        with st.spinner("Evaluating..."):
                            simulator = MockInterviewSimulator()
                            simulator.current_session = session
                            result = simulator.submit_answer(user_answer)
                            
                            feedback = result.get("feedback", {})
                            
                            st.success("✅ Answer received!")
                            
                            col_score, col_coverage = st.columns(2)
                            with col_score:
                                score = feedback.get('score', 0)
                                st.metric("Score", f"{score}/10")
                            with col_coverage:
                                coverage = feedback.get('coverage', 0)
                                st.metric("Coverage", f"{coverage}%")
                            
                            st.markdown(f"**Feedback:** {feedback.get('feedback', 'N/A')}")
                            
                            if feedback.get('strengths'):
                                st.markdown("**✅ What you did well:**")
                                for s in feedback.get('strengths', []):
                                    st.write(f"- {s}")
                            
                            if feedback.get('weaknesses'):
                                st.markdown("**❌ Areas to improve:**")
                                for w in feedback.get('weaknesses', []):
                                    st.write(f"- {w}")
                            
                            if not result.get("is_last_question"):
                                st.session_state.mock_interview_session = simulator.current_session
                                if st.button("➡️ Next Question"):
                                    st.rerun()
                            else:
                                st.markdown("---")
                                st.markdown("### 📊 Interview Results")
                                results = result.get("interview_results", {})
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Average Score", f"{results.get('average_score', 0)}/10")
                                with col2:
                                    st.metric("Total Questions", results.get('total_questions', 0))
                                with col3:
                                    st.metric("Readiness", results.get('readiness_level', 'Not Ready'))
                                
                                st.success(results.get('feedback_summary', ''))
                                
                                st.markdown("**📈 Your Scores:**")
                                st.write(results.get('individual_scores', []))
                                
                                st.markdown("**Focus Areas:**")
                                for area in results.get('improvement_areas', []):
                                    st.write(f"- {area}")
                                
                                if st.button("🔄 Start New Interview"):
                                    st.session_state.mock_interview_session = None
                                    st.rerun()
            
            with col2:
                if st.button("⏭️ Skip Question"):
                    simulator = MockInterviewSimulator()
                    simulator.current_session = session
                    simulator.current_session["current_index"] += 1
                    st.session_state.mock_interview_session = simulator.current_session
                    st.rerun()
            
            with col3:
                if st.button("❌ End Interview"):
                    st.session_state.mock_interview_session = None
                    st.rerun()


def render_about():
    st.title("ℹ️ About AIPS")
    
    st.markdown("""
    ## AI Interview Prep Suite
    
    **Version:** 1.0.0  
    **Status:** MVP for Hackathon
    
    ### 🎯 Mission
    Democratize access to quality interview preparation through AI-powered, personalized guidance.
    
    ### ✨ Features
    
    1. **Resume Builder** - Generate ATS-friendly resumes with AI optimization
    2. **Interview Q&A** - Practice with AI-generated questions and get detailed feedback
    3. **Study Concepts** - Structured learning paths organized by role and difficulty
    4. **Mock Interview** - Realistic interview simulation with scoring and feedback
    
    ### 🛠️ Technology Stack
    - **Frontend:** Streamlit
    - **Backend:** Python with FastAPI (ready)
    - **LLM:** Groq API (LLaMA/Mistral) or Google Gemini
    - **Data:** HuggingFace, Kaggle, GitHub datasets
    
    ### 🚀 Roadmap
    - ✅ Resume generation and optimization
    - ✅ Interview Q&A practice
    - ✅ Study concepts and learning paths
    - ✅ Mock interview simulation
    - ⏳ Voice-based mock interviews
    - ⏳ Skill gap analysis
    - ⏳ Performance analytics dashboard
    - ⏳ PDF export
    
    ### 📝 How to Get Started
    
    1. **Set your API key** in the sidebar (Groq recommended for speed)
    2. **Start with Resume Builder** to create your profile
    3. **Explore Study Concepts** relevant to your role
    4. **Practice with Interview Q&A** for specific questions
    5. **Take a Mock Interview** to assess readiness
    
    ### 🎓 Resources Used
    - LangChain for LLM orchestration
    - Streamlit for rapid UI development
    - Groq API for fast inference
    - Various open-source LLM models
    
    ### 💡 Tips for Best Results
    - Be specific in your answers
    - Use the STAR method (Situation, Task, Action, Result)
    - Review feedback and adjust your approach
    - Practice multiple times with different roles
    
    ---
    
    **Built for the AI Interview Prep Hackathon**
    
    Feel free to provide feedback or suggest improvements!
    """)


# Route to correct page
if current_page == "home":
    render_home()
elif current_page == "resume":
    render_resume_builder()
elif current_page == "interview_qa":
    render_interview_qa()
elif current_page == "study":
    render_study_concepts()
elif current_page == "mock":
    render_mock_interview()
elif current_page == "about":
    render_about()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
Built with ❤️ for Interview Preparation | Powered by AI
</div>
""", unsafe_allow_html=True)
