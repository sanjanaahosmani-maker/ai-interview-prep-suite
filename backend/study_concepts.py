"""
Study Concepts Module
Provides structured study material and learning paths
"""

from typing import Dict, List
from llm_service import LLMService


class StudyConceptsCurator:
    """Curate and organize study material for roles"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def get_study_path(self, role: str, experience_level: str) -> Dict:
        """
        Get structured learning path for a role
        
        Args:
            role: Target job role
            experience_level: Current experience level
        
        Returns:
            Dictionary with organized concepts by difficulty
        """
        concepts = self.llm_service.generate_study_concepts(role, experience_level)
        
        if not concepts or not any(concepts.values()):
            concepts = self._get_fallback_concepts(role, experience_level)
        
        return concepts
    
    def get_topic_details(self, topic: str, role: str) -> Dict:
        """
        Get detailed information about a specific topic
        
        Args:
            topic: Topic name
            role: Context role
        
        Returns:
            Dictionary with topic details, examples, resources
        """
        return {
            "topic": topic,
            "description": f"Detailed explanation of {topic} for {role}",
            "key_concepts": self._get_key_concepts(topic),
            "example_problems": self._get_example_problems(topic),
            "common_mistakes": self._get_common_mistakes(topic),
            "resources": self._get_resources(topic)
        }
    
    def _get_fallback_concepts(self, role: str, level: str) -> Dict:
        """Fallback concepts if LLM fails"""
        concepts = {
            "frontend_developer": {
                "beginner": [
                    {
                        "topic": "HTML Fundamentals",
                        "description": "Learn HTML structure, semantic elements, and form basics",
                        "importance": "Foundation for all web development",
                        "key_points": ["Document structure", "Semantic HTML", "Accessibility"],
                        "resources": ["MDN HTML Guide", "W3C Standards"]
                    },
                    {
                        "topic": "CSS Basics",
                        "description": "Styling with CSS, selectors, box model, flexbox",
                        "importance": "Essential for styling and layout",
                        "key_points": ["Selectors", "Box model", "Flexbox", "Grid"],
                        "resources": ["CSS-Tricks", "MDN CSS"]
                    },
                    {
                        "topic": "JavaScript Fundamentals",
                        "description": "Variables, functions, objects, arrays, ES6+",
                        "importance": "Core language for frontend development",
                        "key_points": ["Variables", "Functions", "Objects", "Async/Await"],
                        "resources": ["JavaScript.info", "MDN"]
                    }
                ],
                "intermediate": [
                    {
                        "topic": "React Basics",
                        "description": "Components, JSX, hooks, state management",
                        "importance": "Most popular frontend framework",
                        "key_points": ["Components", "Hooks", "State", "Props"],
                        "resources": ["Official React Docs", "React Tutorial"]
                    },
                    {
                        "topic": "API Integration",
                        "description": "Fetch API, axios, handling responses, error handling",
                        "importance": "Critical for real-world applications",
                        "key_points": ["REST APIs", "Fetch", "Error Handling"],
                        "resources": ["MDN Fetch API", "API Design Guides"]
                    }
                ],
                "advanced": [
                    {
                        "topic": "Performance Optimization",
                        "description": "Lazy loading, code splitting, caching strategies",
                        "importance": "Build production-ready applications",
                        "key_points": ["Rendering optimization", "Bundle optimization"],
                        "resources": ["Web Vitals", "Performance best practices"]
                    }
                ]
            },
            "backend_developer": {
                "beginner": [
                    {
                        "topic": "Server Fundamentals",
                        "description": "HTTP protocol, REST APIs, client-server architecture",
                        "importance": "Foundation of backend development",
                        "key_points": ["HTTP methods", "REST principles", "Status codes"],
                        "resources": ["HTTP MDN", "REST guide"]
                    },
                    {
                        "topic": "Database Basics",
                        "description": "Relational databases, SQL basics, CRUD operations",
                        "importance": "Data persistence and management",
                        "key_points": ["SQL", "Schemas", "Queries"],
                        "resources": ["SQL Tutorial", "Database Design"]
                    }
                ],
                "intermediate": [
                    {
                        "topic": "API Design",
                        "description": "RESTful API design, authentication, versioning",
                        "importance": "Design scalable APIs",
                        "key_points": ["Design patterns", "Security", "Versioning"],
                        "resources": ["API Design Guide", "OAuth"]
                    }
                ],
                "advanced": [
                    {
                        "topic": "System Design",
                        "description": "Scaling, load balancing, microservices, caching",
                        "importance": "Handle high-scale systems",
                        "key_points": ["Architecture", "Caching", "Message queues"],
                        "resources": ["System Design Primer", "Distributed systems"]
                    }
                ]
            },
            "data_analyst": {
                "beginner": [
                    {
                        "topic": "SQL Fundamentals",
                        "description": "SELECT, WHERE, JOIN, GROUP BY, ORDER BY",
                        "importance": "Essential skill for data work",
                        "key_points": ["Queries", "Joins", "Aggregations"],
                        "resources": ["SQL Tutorial", "LeetCode Database"]
                    },
                    {
                        "topic": "Excel for Data",
                        "description": "Formulas, pivot tables, data cleaning",
                        "importance": "Common tool in organizations",
                        "key_points": ["Formulas", "Pivot tables", "Analysis"],
                        "resources": ["Excel tutorials"]
                    }
                ],
                "intermediate": [
                    {
                        "topic": "Data Visualization",
                        "description": "Tableau, Power BI, dashboard creation",
                        "importance": "Communicate insights effectively",
                        "key_points": ["Dashboard design", "Visual best practices"],
                        "resources": ["Tableau public", "Power BI docs"]
                    }
                ],
                "advanced": [
                    {
                        "topic": "Statistical Analysis",
                        "description": "Hypothesis testing, A/B testing, regression",
                        "importance": "Advanced analytical skills",
                        "key_points": ["Statistics", "Testing", "Modeling"],
                        "resources": ["Statistics guide", "A/B testing"]
                    }
                ]
            }
        }
        
        role_key = role.lower().split()[0] if role else "frontend"
        return concepts.get(role_key + "_" + role.lower().replace(" ", "_"), concepts.get("frontend_developer", {}))
    
    def _get_key_concepts(self, topic: str) -> List[str]:
        """Get key concepts for a topic"""
        return [f"Concept 1 related to {topic}", f"Concept 2 related to {topic}"]
    
    def _get_example_problems(self, topic: str) -> List[str]:
        """Get example problems for a topic"""
        return [f"Example problem 1 for {topic}", f"Example problem 2 for {topic}"]
    
    def _get_common_mistakes(self, topic: str) -> List[str]:
        """Get common mistakes for a topic"""
        return [f"Common mistake 1 in {topic}", f"Common mistake 2 in {topic}"]
    
    def _get_resources(self, topic: str) -> List[Dict]:
        """Get learning resources for a topic"""
        return [
            {"name": "Official Documentation", "type": "docs", "url": "#"},
            {"name": "YouTube Tutorial", "type": "video", "url": "#"},
            {"name": "Practice Problems", "type": "practice", "url": "#"}
        ]
