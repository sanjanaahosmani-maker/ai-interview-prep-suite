"""
Quick Start Script for AI Interview Prep Suite
Run this to test the application components
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from llm_service import LLMService
from resume_builder import ResumeBuilder
from question_generator import QuestionGenerator, MockInterviewSimulator
from study_concepts import StudyConceptsCurator


def demo_resume_builder():
    """Demo resume building functionality"""
    print("\n" + "="*60)
    print("DEMO 1: Resume Builder")
    print("="*60)
    
    builder = ResumeBuilder()
    
    profile = {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "+1-555-0123",
        "target_role": "Frontend Developer",
        "experience": "2 years as Junior Developer at TechCorp",
        "education": "B.Tech Computer Science, 2022",
        "skills": "React, JavaScript, TypeScript, Tailwind CSS, HTML, CSS, Git",
        "projects": "E-commerce platform using React and Node.js, Personal portfolio website",
        "certifications": "AWS Certified Cloud Practitioner"
    }
    
    print("\nGenerating resume...")
    resume = builder.build_resume(profile)
    print("\n✅ Resume Generated!")
    print(resume[:500] + "..." if len(resume) > 500 else resume)


def demo_interview_questions():
    """Demo interview question generation"""
    print("\n" + "="*60)
    print("DEMO 2: Interview Q&A Generator")
    print("="*60)
    
    gen = QuestionGenerator()
    
    print("\nGenerating questions for Frontend Developer (Mid-level)...")
    questions = gen.generate_questions(
        role="Frontend Developer",
        experience_level="mid",
        domain="Web Development",
        count=3
    )
    
    print(f"\n✅ Generated {len(questions)} questions!")
    
    for i, q in enumerate(questions[:2], 1):
        print(f"\nQuestion {i}: {q.get('question', 'N/A')[:60]}...")
        print(f"Key Points: {q.get('key_points', [])[:2]}")


def demo_study_concepts():
    """Demo study concepts"""
    print("\n" + "="*60)
    print("DEMO 3: Study Concepts")
    print("="*60)
    
    curator = StudyConceptsCurator()
    
    print("\nGenerating study path for Backend Developer (Intermediate)...")
    concepts = curator.get_study_path("Backend Developer", "intermediate")
    
    print(f"\n✅ Study path generated!")
    
    if concepts.get('beginner'):
        print(f"\n📍 Beginner Topics: {len(concepts['beginner'])} topics")
        for topic in concepts['beginner'][:1]:
            print(f"  - {topic.get('topic', 'N/A')}")
    
    if concepts.get('intermediate'):
        print(f"📍 Intermediate Topics: {len(concepts['intermediate'])} topics")
        for topic in concepts['intermediate'][:1]:
            print(f"  - {topic.get('topic', 'N/A')}")


def demo_mock_interview():
    """Demo mock interview"""
    print("\n" + "="*60)
    print("DEMO 4: Mock Interview Simulator")
    print("="*60)
    
    simulator = MockInterviewSimulator()
    
    print("\nStarting mock interview...")
    session_info = simulator.start_interview(
        role="Data Analyst",
        experience_level="junior",
        domain="Business Intelligence",
        num_questions=2
    )
    
    print(f"\n✅ Interview started!")
    print(f"Total Questions: {session_info['total_questions']}")
    print(f"Question 1 of {session_info['total_questions']}")
    print(f"Q: {session_info['question']}")


if __name__ == "__main__":
    print("\n🎯 AI Interview Prep Suite - Feature Demos\n")
    
    try:
        # Note: These demos will work better with API keys configured
        # demo_resume_builder()
        # demo_interview_questions()
        # demo_study_concepts()
        # demo_mock_interview()
        
        print("""
        To run the full application:
        
        1. Set up your API key:
           - Export GROQ_API_KEY=your_key_here
           - Or export GEMINI_API_KEY=your_key_here
        
        2. Run Streamlit app:
           streamlit run frontend/app.py
        
        3. Open browser to http://localhost:8501
        
        Features available:
        - 📄 Resume Builder
        - ❓ Interview Q&A Generator
        - 📚 Study Concepts
        - 🎤 Mock Interview Simulator
        """)
        
    except Exception as e:
        print(f"⚠️  Demo error: {e}")
        print("\nMake sure you have API keys configured for full functionality.")
