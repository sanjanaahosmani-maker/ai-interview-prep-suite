"""
Flask Quick Start for AI Interview Prep Suite
=============================================

This script demonstrates how to use the Flask application and test the endpoints.
"""

import os
import sys
import requests
import json

# Configuration
API_BASE = 'http://localhost:5000'
DEMO_API_KEY = 'your_test_api_key'

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def test_health_check():
    """Test health check endpoint"""
    print_header("1. Health Check")
    
    try:
        response = requests.get(f'{API_BASE}/api/health')
        data = response.json()
        print(f"✓ Status: {data.get('status')}")
        print(f"✓ Service: {data.get('service')}")
        print(f"✓ Version: {data.get('version')}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_resume_generation():
    """Test resume generation endpoint"""
    print_header("2. Resume Generation")
    
    profile = {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "+1-555-0123",
        "target_role": "Frontend Developer",
        "experience": "2 years as Junior Developer at TechCorp",
        "education": "B.Tech Computer Science, 2022",
        "skills": "React, JavaScript, TypeScript, HTML, CSS, Git",
        "projects": "E-commerce platform using React",
        "certifications": "AWS Certified Cloud Practitioner"
    }
    
    print("Sending profile:")
    print(json.dumps(profile, indent=2))
    print("\nGenerating resume...")
    
    try:
        response = requests.post(
            f'{API_BASE}/api/resume/generate',
            json=profile
        )
        data = response.json()
        
        if data.get('success'):
            print(f"✓ Resume generated successfully!")
            print(f"✓ Length: {len(data.get('resume', ''))} characters")
            print(f"\nResume preview:\n{data.get('resume', '')[:300]}...")
            return True
        else:
            print(f"✗ Error: {data.get('error')}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_interview_questions():
    """Test interview question generation"""
    print_header("3. Interview Questions Generation")
    
    params = {
        "role": "Frontend Developer",
        "experience_level": "mid",
        "domain": "Web Development",
        "count": 3
    }
    
    print("Generating questions for:")
    print(f"  Role: {params['role']}")
    print(f"  Level: {params['experience_level']}")
    print(f"  Count: {params['count']}\n")
    
    try:
        response = requests.post(
            f'{API_BASE}/api/interview/questions',
            json=params
        )
        data = response.json()
        
        if data.get('success'):
            questions = data.get('questions', [])
            print(f"✓ Generated {len(questions)} questions!\n")
            
            for i, q in enumerate(questions[:2], 1):
                print(f"Question {i}:")
                print(f"  {q.get('question', 'N/A')[:100]}...")
                print()
            
            return True
        else:
            print(f"✗ Error: {data.get('error')}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_study_concepts():
    """Test study concepts endpoint"""
    print_header("4. Study Concepts")
    
    params = {
        "role": "Frontend Developer",
        "experience_level": "intermediate"
    }
    
    print("Loading study path for:")
    print(f"  Role: {params['role']}")
    print(f"  Level: {params['experience_level']}\n")
    
    try:
        response = requests.post(
            f'{API_BASE}/api/study/concepts',
            json=params
        )
        data = response.json()
        
        if data.get('success'):
            concepts = data.get('concepts', {})
            print(f"✓ Study path loaded!")
            print(f"✓ Total concepts: {sum(len(v) if isinstance(v, list) else 0 for v in concepts.values())}")
            print(f"✓ Difficulty levels: {list(concepts.keys())}")
            return True
        else:
            print(f"✗ Error: {data.get('error')}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_mock_interview():
    """Test mock interview endpoints"""
    print_header("5. Mock Interview Session")
    
    # Start mock interview
    start_params = {
        "role": "Backend Developer",
        "experience_level": "junior",
        "domain": "Python & APIs",
        "num_questions": 2
    }
    
    print("Starting mock interview:")
    print(f"  Role: {start_params['role']}")
    print(f"  Questions: {start_params['num_questions']}\n")
    
    try:
        response = requests.post(
            f'{API_BASE}/api/mock-interview/start',
            json=start_params
        )
        data = response.json()
        
        if not data.get('success'):
            print(f"✗ Error: {data.get('error')}")
            return False
        
        session_id = data.get('session_id')
        print(f"✓ Session started!")
        print(f"✓ Session ID: {session_id}")
        print(f"✓ Current question: {data.get('current_question_index', 0) + 1}/{data.get('total_questions')}\n")
        
        # Print first question
        current_q = data.get('current_question', {})
        if current_q:
            print(f"Question: {current_q.get('question', 'N/A')[:100]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_get_roles():
    """Test get roles endpoint"""
    print_header("6. Get Available Roles")
    
    try:
        response = requests.get(f'{API_BASE}/api/roles')
        data = response.json()
        
        if data.get('success'):
            roles = data.get('roles', [])
            print(f"✓ Available roles ({len(roles)}):")
            for role in roles[:5]:
                print(f"  • {role}")
            if len(roles) > 5:
                print(f"  ... and {len(roles) - 5} more")
            return True
        else:
            print(f"✗ Error: {data.get('error')}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" Flask AI Interview Prep Suite - API Test Suite")
    print("="*70)
    
    print("\n📋 Testing Flask API endpoints...")
    print(f"🔗 API Base URL: {API_BASE}")
    print("\n⚠️  Make sure the Flask server is running!")
    print("   Run: python backend/flask_app.py\n")
    
    input("Press Enter to start tests...")
    
    results = {
        "Health Check": test_health_check(),
        "Resume Generation": test_resume_generation(),
        "Interview Questions": test_interview_questions(),
        "Study Concepts": test_study_concepts(),
        "Mock Interview": test_mock_interview(),
        "Get Roles": test_get_roles(),
    }
    
    # Summary
    print_header("Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*70}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{'='*70}\n")
    
    if passed == total:
        print("🎉 All tests passed! Flask API is working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please check the errors above.")

if __name__ == '__main__':
    main()
