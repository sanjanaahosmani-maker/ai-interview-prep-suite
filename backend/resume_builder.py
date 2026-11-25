"""
Resume Builder Module
Handles resume generation and optimization
"""

from typing import Dict, List
from llm_service import LLMService


class ResumeBuilder:
    """Resume generation and optimization"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def build_resume(self, user_profile: Dict) -> str:
        """
        Generate resume from user profile
        
        Args:
            user_profile: User input containing education, experience, skills, etc.
        
        Returns:
            Formatted resume text
        """
        # Validate input
        if not self._validate_profile(user_profile):
            return "Invalid profile. Please fill in required fields."
        
        # Try LLM first, with comprehensive error handling
        try:
            resume = self.llm_service.generate_resume(user_profile)
            # Validate response
            if resume and isinstance(resume, str) and len(resume) > 20:
                # Check if it looks like a valid resume (not an error message)
                if not any(msg in resume.lower() for msg in ['error', 'api error', '429', 'quota']):
                    return resume
        except Exception as e:
            error_msg = str(e).lower()
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"LLM generation failed: {error_msg}. Using fallback template generation.")
            # Fall through to template generation
        
        # Fallback: Use template-based generation (no API calls)
        return self._generate_resume_template(user_profile)
    
    def _generate_resume_template(self, profile: Dict) -> str:
        """
        Generate resume using template (fallback when LLM fails)
        """
        name = profile.get('name', '').strip()
        target_role = profile.get('target_role', '').strip()
        education = profile.get('education', '').strip()
        experience = profile.get('experience', '').strip()
        skills = profile.get('skills', '').strip()
        projects = profile.get('projects', '').strip()
        certifications = profile.get('certifications', '').strip()
        
        resume = f"""## Professional Summary

Dedicated {target_role} with strong technical expertise and proven ability to deliver high-quality solutions. Seeking to leverage skills in {self._first_skill(skills)} and related technologies to contribute to innovative projects and achieve organizational goals.

## Work Experience

{experience if experience else '- Experienced professional with strong problem-solving abilities'}

## Education

{education if education else '- Education background in relevant field'}

## Technical Skills

{self._format_skills(skills)}

"""
        
        if projects:
            resume += f"""## Projects

{projects}

"""
        
        if certifications:
            resume += f"""## Certifications

{certifications}"""
        
        return resume.strip()
    
    def _first_skill(self, skills_text: str) -> str:
        """Extract first skill from comma-separated list"""
        if not skills_text:
            return "software development"
        first_skill = skills_text.split(',')[0].strip()
        return first_skill if first_skill else "software development"
    
    def _format_skills(self, skills_text: str) -> str:
        """Format skills into categories"""
        if not skills_text:
            return "- Strong technical foundation"
        
        skills_list = [s.strip() for s in skills_text.split(',')]
        
        # Group skills
        programming = []
        frameworks = []
        tools = []
        other = []
        
        framework_keywords = ['react', 'vue', 'angular', 'node', 'express', 'django', 'flask', 'spring']
        tool_keywords = ['docker', 'git', 'sql', 'mongodb', 'aws', 'ci/cd', 'jenkins']
        
        for skill in skills_list:
            skill_lower = skill.lower()
            if any(fw in skill_lower for fw in framework_keywords):
                frameworks.append(skill)
            elif any(t in skill_lower for t in tool_keywords):
                tools.append(skill)
            elif any(lang in skill_lower for lang in ['python', 'javascript', 'java', 'c++', 'typescript']):
                programming.append(skill)
            else:
                other.append(skill)
        
        result = []
        if programming:
            result.append(f"- **Programming Languages:** {', '.join(programming)}")
        if frameworks:
            result.append(f"- **Frameworks & Libraries:** {', '.join(frameworks)}")
        if tools:
            result.append(f"- **Tools & Technologies:** {', '.join(tools)}")
        if other:
            result.append(f"- **Other Skills:** {', '.join(other)}")
        
        return '\n'.join(result) if result else "- Technical skills across multiple domains"
    
    def optimize_resume(self, resume_text: str, target_role: str) -> Dict:
        """
        Suggest improvements to resume
        
        Args:
            resume_text: Current resume text
            target_role: Target job role
        
        Returns:
            Dictionary with suggestions
        """
        # This would call LLM for optimization suggestions
        suggestions = {
            "keywords": self._extract_missing_keywords(target_role),
            "action_verbs": self._suggest_action_verbs(),
            "improvements": [
                "Quantify achievements with specific metrics",
                "Use industry-specific keywords",
                "Tailor summary to target role",
                "Highlight relevant skills prominently"
            ]
        }
        return suggestions
    
    def _validate_profile(self, profile: Dict) -> bool:
        """Validate user profile completeness"""
        required_fields = ["name", "email", "target_role"]
        return all(profile.get(field) for field in required_fields)
    
    def _extract_missing_keywords(self, role: str) -> List[str]:
        """Extract keywords that should be in resume for given role"""
        role_keywords = {
            "frontend developer": ["React", "Vue", "Angular", "TypeScript", "CSS", "HTML", "Responsive Design"],
            "backend developer": ["Python", "Node.js", "Java", "APIs", "Databases", "SQL"],
            "data analyst": ["SQL", "Python", "Tableau", "Power BI", "Statistics", "Data Visualization"],
            "data scientist": ["Machine Learning", "Python", "TensorFlow", "Statistics", "Deep Learning"],
            "full stack developer": ["React", "Node.js", "MongoDB", "SQL", "APIs", "DevOps"]
        }
        return role_keywords.get(role.lower(), [])
    
    def _suggest_action_verbs(self) -> List[str]:
        """Get action verbs for resume"""
        return [
            "Developed", "Designed", "Implemented", "Optimized", "Enhanced",
            "Led", "Managed", "Collaborated", "Spearheaded", "Architected",
            "Automated", "Improved", "Analyzed", "Created", "Built"
        ]
    
    def export_to_pdf(self, resume_text: str, filename: str) -> bool:
        """Export resume to PDF"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            
            # Simple text wrapping and writing
            y = height - 40
            lines = resume_text.split('\n')
            
            for line in lines:
                if y < 40:
                    c.showPage()
                    y = height - 40
                c.drawString(40, y, line[:80])  # Limit line length
                y -= 15
            
            c.save()
            return True
        except Exception as e:
            print(f"Error exporting to PDF: {e}")
            return False
