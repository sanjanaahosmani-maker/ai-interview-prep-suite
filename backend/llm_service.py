"""
LLM Service for AI Interview Prep Suite
Handles all interactions with Groq/Gemini APIs
"""

import os
import logging
from typing import Optional
import json

# Ensure .env is loaded regardless of import order
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)


class LLMService:
    """Service to handle LLM API calls"""
    
    def __init__(self):
        """Initialize LLM service with appropriate API"""
        self.provider = os.getenv(
            "LLM_PROVIDER",
            "groq" if os.getenv("GROQ_API_KEY") else "gemini"
        ).strip().lower()
        self.use_groq = self.provider == "groq"
        self.client = None
        
        if self.use_groq:
            try:
                import groq
                self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY", ""))
                self.groq_model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
                logger.info("Groq client initialized with model: %s", self.groq_model)
            except ImportError:
                logger.error("groq package not installed.")
        elif self.provider == "gemini":
            try:
                import warnings
                warnings.filterwarnings('ignore', category=FutureWarning)
                import google.generativeai as genai
                api_key = os.getenv("GEMINI_API_KEY", "")
                if not api_key:
                    logger.error("GEMINI_API_KEY not set in environment.")
                else:
                    genai.configure(api_key=api_key)
                    self.client = genai.GenerativeModel('gemini-2.0-flash-lite')
                    self.gemini_model = 'gemini-2.0-flash-lite'
                    logger.info("Gemini client initialized with model: gemini-2.0-flash-lite")
            except ImportError:
                logger.error("google-generativeai package not installed.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
        else:
            logger.error("Unsupported LLM_PROVIDER: %s", self.provider)

    
    def generate_resume(self, user_profile: dict) -> str:
        """
        Generate ATS-friendly resume from user profile
        
        Args:
            user_profile: Dictionary with name, email, phone, experience, education, skills, projects, target_role
        
        Returns:
            Generated resume as formatted string
        """
        prompt = self._build_resume_prompt(user_profile)
        return self._call_llm(prompt)
    
    def generate_interview_questions(self, role: str, experience_level: str, domain: str, count: int = 5) -> list:
        """
        Generate role-specific interview questions
        
        Args:
            role: Job role (e.g., "Frontend Developer")
            experience_level: "junior", "mid", "senior"
            domain: Domain/industry
            count: Number of questions to generate
        
        Returns:
            List of interview questions with ideal answers
        """
        prompt = self._build_question_prompt(role, experience_level, domain, count)
        response = self._call_llm(prompt)
        return self._parse_questions(response)
    
    def generate_study_concepts(self, role: str, experience_level: str) -> dict:
        """
        Generate structured study concepts for a role
        
        Args:
            role: Target job role
            experience_level: Experience level
        
        Returns:
            Dictionary of topics and concepts organized by difficulty
        """
        prompt = self._build_concepts_prompt(role, experience_level)
        response = self._call_llm(prompt)
        return self._parse_concepts(response)
    
    def evaluate_mock_interview_response(self, question: str, user_answer: str, ideal_answer: str) -> dict:
        """
        Evaluate user's mock interview response
        
        Args:
            question: Interview question
            user_answer: User's response
            ideal_answer: Ideal/model answer
        
        Returns:
            Dictionary with score, feedback, strengths, weaknesses
        """
        prompt = self._build_evaluation_prompt(question, user_answer, ideal_answer)
        response = self._call_llm(prompt)
        return self._parse_evaluation(response)
    
    def _call_llm(self, prompt: str) -> str:
        """Make LLM API call"""
        if not self.client:
            return "LLM service not initialized. Please set up your API keys."
        
        try:
            logger.info(f"Calling LLM with prompt length: {len(prompt)} chars")
            logger.info(f"Using {'Groq' if self.use_groq else 'Gemini'} API")
            
            if self.use_groq:
                message = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.groq_model,
                    temperature=0.7,
                    max_tokens=2048
                )
                result = message.choices[0].message.content
            else:
                response = self.client.generate_content(prompt)
                result = response.text
            
            logger.info(f"LLM returned {len(result)} chars")
            return result
        except Exception as e:
            logger.error(f"LLM API Error: {str(e)}", exc_info=True)
            raise Exception(f"LLM API Error: {str(e)}")
    
    def _build_resume_prompt(self, profile: dict) -> str:
        """Build prompt for resume generation"""
        name = profile.get('name', 'N/A')
        target_role = profile.get('target_role', 'N/A')
        experience = profile.get('experience', 'N/A')
        education = profile.get('education', 'N/A')
        skills = profile.get('skills', 'N/A')
        projects = profile.get('projects', 'N/A')
        certifications = profile.get('certifications', '')

        cert_section = f"\nCertifications: {certifications}" if certifications else ""

        return f"""Generate a professional, ATS-optimized resume in Markdown format.

**Candidate Profile:**
- Name: {name}
- Target Role: {target_role}
- Experience: {experience}
- Education: {education}
- Skills: {skills}
- Projects: {projects}{cert_section}

**CRITICAL REQUIREMENTS:**
1. Include ONLY professional sections - NO personal hobbies, interests, or non-work details
2. Do NOT include contact information (email, phone) in the resume content
3. Output format MUST be clean Markdown with only these sections (in order):
   - Professional Summary (1-2 sentences max, tailored to {target_role})
   - Work Experience (bullet points with metrics/results)
   - Education
   - Technical Skills (grouped by category)
   - Projects (if provided)
   - Certifications (if provided)
4. Use strong action verbs: Developed, Designed, Implemented, Optimized, Led, etc.
5. Include quantifiable achievements and metrics where possible
6. Keep total length concise - focus on relevance to {target_role}
7. ATS-optimized: use standard keywords relevant to {target_role}
8. Do NOT invent or add any information not explicitly provided
9. Formatting: Use ## for section headers, - for bullet points only
10. Professional tone throughout - no casual language

Generate the resume now:"""

    def _build_question_prompt(self, role: str, level: str, domain: str, count: int) -> str:
        """Build prompt for interview question generation"""
        return f"""Generate {count} interview questions for a {level} {role} in {domain}.

For each question, provide:
1. The question itself
2. An ideal/model answer (2-3 paragraphs)
3. Key points to cover
4. Evaluation criteria (what makes a good answer)

Format as JSON array with structure:
[
  {{
    "question": "...",
    "ideal_answer": "...",
    "key_points": ["point1", "point2", ...],
    "evaluation_criteria": ["criterion1", "criterion2", ...]
  }},
  ...
]

Include a mix of:
- Technical questions specific to {role}
- Behavioral questions
- Problem-solving scenarios
- Domain-specific challenges"""

    def _build_concepts_prompt(self, role: str, level: str) -> str:
        """Build prompt for study concepts generation"""
        return f"""Create a structured learning path for a {level}-level candidate preparing for {role}.

Organize concepts by difficulty levels: Beginner, Intermediate, Advanced

For each concept, provide:
1. Name of the concept/topic
2. Brief description (2-3 lines)
3. Why it's important for {role}
4. Key points to remember
5. Suggested study resources/topics

Format as JSON:
{{
  "beginner": [
    {{
      "topic": "...",
      "description": "...",
      "importance": "...",
      "key_points": ["point1", "point2", ...],
      "resources": ["resource1", "resource2", ...]
    }},
    ...
  ],
  "intermediate": [...],
  "advanced": [...]
}}"""

    def _build_evaluation_prompt(self, question: str, user_answer: str, ideal_answer: str) -> str:
        """Build prompt for response evaluation"""
        return f"""Evaluate this mock interview response:

Question: {question}

User's Answer: {user_answer}

Model Answer: {ideal_answer}

Provide evaluation in JSON format:
{{
  "score": (out of 10),
  "strengths": ["strength1", "strength2", ...],
  "weaknesses": ["weakness1", "weakness2", ...],
  "feedback": "Detailed constructive feedback...",
  "suggestions": ["suggestion1", "suggestion2", ...],
  "coverage": (percentage of model answer covered)
}}

Be constructive and helpful while being honest about areas for improvement."""

    def _parse_questions(self, response: str) -> list:
        """Parse LLM response into questions list"""
        try:
            # Try to extract JSON from response
            start = response.find('[')
            end = response.rfind(']') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        return []
    
    def _parse_concepts(self, response: str) -> dict:
        """Parse LLM response into concepts dict"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        return {"beginner": [], "intermediate": [], "advanced": []}
    
    def _parse_evaluation(self, response: str) -> dict:
        """Parse LLM response into evaluation dict"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        return {
            "score": 0,
            "strengths": [],
            "weaknesses": [],
            "feedback": "Unable to parse evaluation",
            "suggestions": [],
            "coverage": 0
        }
