"""
Interview Question Generator Module
Generates role-specific interview questions and answers
"""

from typing import List, Dict
from llm_service import LLMService


class QuestionGenerator:
    """Generate interview questions and provide feedback"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.questions_cache = {}
    
    def generate_questions(self, role: str, experience_level: str, domain: str, count: int = 5) -> List[Dict]:
        """
        Generate interview questions for a specific role
        
        Args:
            role: Job role (e.g., "Frontend Developer")
            experience_level: "junior", "mid", "senior"
            domain: Domain/industry
            count: Number of questions
        
        Returns:
            List of question dictionaries with ideal answers
        """
        questions = self.llm_service.generate_interview_questions(
            role, experience_level, domain, count
        )
        
        # Cache for reference
        cache_key = f"{role}_{experience_level}_{domain}"
        self.questions_cache[cache_key] = questions
        
        return questions if questions else self._get_fallback_questions(role, experience_level)
    
    def get_question_feedback(self, question: str, user_answer: str, ideal_answer: str) -> Dict:
        """
        Get feedback on user's answer to an interview question
        
        Args:
            question: The interview question
            user_answer: User's response
            ideal_answer: Model/ideal answer
        
        Returns:
            Feedback dictionary with score, suggestions, etc.
        """
        feedback = self.llm_service.evaluate_mock_interview_response(
            question, user_answer, ideal_answer
        )
        return feedback
    
    def _get_fallback_questions(self, role: str, level: str) -> List[Dict]:
        """Fallback questions if LLM generation fails"""
        fallback = {
            "junior_frontend": [
                {
                    "question": "What is the difference between let, const, and var in JavaScript?",
                    "ideal_answer": "var is function-scoped and hoisted, let and const are block-scoped. const is immutable and should be preferred for modern JavaScript.",
                    "key_points": ["Scope differences", "Hoisting", "Mutability"],
                    "evaluation_criteria": ["Understands scoping rules", "Knows best practices"]
                },
                {
                    "question": "Explain the box model in CSS.",
                    "ideal_answer": "The box model consists of content, padding, border, and margin. Understanding this is crucial for layout and spacing in web design.",
                    "key_points": ["Content", "Padding", "Border", "Margin"],
                    "evaluation_criteria": ["Can explain each component", "Understands how they affect layout"]
                }
            ],
            "mid_backend": [
                {
                    "question": "Explain database normalization and its benefits.",
                    "ideal_answer": "Normalization organizes data to minimize redundancy through normal forms (1NF, 2NF, 3NF). It improves data integrity and query efficiency.",
                    "key_points": ["Reduces redundancy", "Improves integrity", "Normal forms"],
                    "evaluation_criteria": ["Understands normal forms", "Can explain trade-offs"]
                }
            ],
            "senior_data_science": [
                {
                    "question": "Walk us through your approach to building a recommendation system.",
                    "ideal_answer": "Start with problem definition, data collection, feature engineering, model selection (collaborative/content-based), evaluation metrics, and deployment considerations.",
                    "key_points": ["Problem analysis", "Methodology", "Trade-offs", "Deployment"],
                    "evaluation_criteria": ["System thinking", "Technical depth", "Business awareness"]
                }
            ]
        }
        
        key = f"{level}_{role.lower().split()[0]}"
        return fallback.get(key, [
            {
                "question": f"Tell us about your experience with {role}.",
                "ideal_answer": "Share relevant projects and achievements.",
                "key_points": ["Experience", "Impact"],
                "evaluation_criteria": ["Relevance", "Clarity"]
            }
        ])


class MockInterviewSimulator:
    """Simulate a mock interview session"""
    
    def __init__(self):
        self.question_generator = QuestionGenerator()
        self.current_session = None
    
    def start_interview(self, role: str, experience_level: str, domain: str, num_questions: int = 5) -> Dict:
        """
        Start a new mock interview session
        
        Args:
            role: Job role
            experience_level: Experience level
            domain: Domain
            num_questions: Number of questions in interview
        
        Returns:
            Session info with first question
        """
        questions = self.question_generator.generate_questions(
            role, experience_level, domain, num_questions
        )
        
        self.current_session = {
            "role": role,
            "experience_level": experience_level,
            "domain": domain,
            "questions": questions,
            "current_index": 0,
            "responses": [],
            "scores": []
        }
        
        return {
            "question_number": 1,
            "total_questions": num_questions,
            "question": questions[0]["question"] if questions else "Unable to generate questions",
            "session_id": hash(str(self.current_session))
        }
    
    def submit_answer(self, answer: str) -> Dict:
        """
        Submit answer to current question and get feedback
        
        Args:
            answer: User's answer to current question
        
        Returns:
            Feedback on answer and next question or results
        """
        if not self.current_session:
            return {"error": "No active interview session"}
        
        current_q_idx = self.current_session["current_index"]
        question_data = self.current_session["questions"][current_q_idx]
        
        # Get feedback on answer
        feedback = self.question_generator.get_question_feedback(
            question_data["question"],
            answer,
            question_data["ideal_answer"]
        )
        
        # Store response
        self.current_session["responses"].append(answer)
        self.current_session["scores"].append(feedback.get("score", 0))
        
        # Prepare next question or results
        self.current_session["current_index"] += 1
        
        result = {
            "feedback": feedback,
            "is_last_question": self.current_session["current_index"] >= len(self.current_session["questions"])
        }
        
        if not result["is_last_question"]:
            next_q = self.current_session["questions"][self.current_session["current_index"]]
            result["next_question"] = {
                "question_number": self.current_session["current_index"] + 1,
                "total_questions": len(self.current_session["questions"]),
                "question": next_q["question"]
            }
        else:
            # Interview complete - generate results
            result["interview_results"] = self._generate_results()
        
        return result
    
    def _generate_results(self) -> Dict:
        """Generate interview results and summary"""
        scores = self.current_session["scores"]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            "average_score": round(avg_score, 1),
            "total_questions": len(self.current_session["questions"]),
            "individual_scores": scores,
            "feedback_summary": "Great effort! Focus on expanding your answers with specific examples.",
            "readiness_level": self._calculate_readiness(avg_score),
            "improvement_areas": ["Add more specific examples", "Expand technical explanations"]
        }
    
    def _calculate_readiness(self, score: float) -> str:
        """Calculate readiness level based on score"""
        if score >= 8:
            return "Highly Ready"
        elif score >= 6:
            return "Ready"
        elif score >= 4:
            return "Moderately Ready"
        else:
            return "Needs Preparation"
