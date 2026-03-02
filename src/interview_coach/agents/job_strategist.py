"""
Job Strategist Agent - Analyzes job descriptions and resumes to predict interview questions
"""
from typing import Dict, List, Any
import re
from ..api_interface import AIInterface


class JobStrategist:
    """Expert HR Consultant agent that analyzes job requirements and user qualifications."""

    def __init__(self):
        self.ai_interface = AIInterface()
        self.system_prompt = """
You are an expert HR Consultant. Your goal is to analyze the provided Job Description and User Resume.

Tasks:
1. Extract the 5 most critical technical skills.
2. Predict 3 behavioral and 2 technical questions specific to this role.
3. Provide a 'Success Metric' for each, explaining what a high-quality answer should look like.

Output: Pass this structured data to the Interviewer agent.
"""

    def analyze(self, job_description: str, resume: str) -> Dict[str, Any]:
        """
        Analyze job description and resume to create interview strategy.

        Args:
            job_description: The job posting content
            resume: The user's resume/CV content

        Returns:
            Dictionary containing interview strategy
        """
        # Extract core competencies from job description
        technical_skills = self._extract_technical_skills(job_description)
        behavioral_skills = self._extract_behavioral_requirements(job_description)

        # Predict questions based on job requirements and user's background
        predicted_questions = self._generate_questions(
            job_description,
            resume,
            technical_skills,
            behavioral_skills
        )

        strategy = {
            "job_description": job_description,
            "resume": resume,
            "core_competencies": {
                "technical_skills": technical_skills[:5],  # Top 5 technical skills
                "behavioral_skills": behavioral_skills
            },
            "predicted_questions": predicted_questions,
            "success_metrics": self._define_success_metrics(predicted_questions)
        }

        return strategy

    def _extract_technical_skills(self, job_description: str) -> List[str]:
        """Extract technical skills from job description."""
        # Look for common technical skill patterns
        tech_patterns = [
            r'\b(Python|Java|JavaScript|TypeScript|C\+\+|C#|Go|Rust|PHP|Ruby)\b',
            r'\b(SQL|NoSQL|MongoDB|PostgreSQL|MySQL|Oracle)\b',
            r'\b(AWS|Azure|GCP|Docker|Kubernetes|CI/CD|Jenkins)\b',
            r'\b(Machine Learning|AI|Data Science|Analytics|React|Angular|Vue|Node\.js)\b',
            r'\b(Software Development|Agile|Scrum|DevOps|Testing|Security)\b',
            r'\b(API|REST|GraphQL|Microservices|Cloud Computing)\b'
        ]

        skills = set()
        for pattern in tech_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            skills.update(match.lower().capitalize() for match in matches)

        # Additional manual parsing for common skills
        job_lower = job_description.lower()
        common_skills = [
            "Leadership", "Communication", "Problem Solving", "Teamwork",
            "Project Management", "Data Analysis", "Design", "Architecture",
            "Troubleshooting", "Mentoring", "Planning", "Coordination"
        ]

        for skill in common_skills:
            if skill.lower() in job_lower:
                skills.add(skill)

        return list(skills)

    def _extract_behavioral_requirements(self, job_description: str) -> List[str]:
        """Extract behavioral competencies from job description."""
        behavioral_keywords = [
            "collaboration", "communication", "leadership", "problem-solving",
            "adaptability", "initiative", "teamwork", "creativity",
            "decision-making", "conflict resolution", "time management",
            "customer focus", "innovation", "accountability"
        ]

        requirements = []
        job_lower = job_description.lower()

        for keyword in behavioral_keywords:
            if keyword in job_lower:
                requirements.append(keyword.title())

        return requirements

    def _generate_questions(self, job_desc: str, resume: str, tech_skills: List[str], behav_skills: List[str]) -> List[Dict[str, str]]:
        """Generate predicted interview questions."""
        questions = []

        # Behavioral questions (3)
        behav_templates = [
            "Tell me about a time when you demonstrated strong {} skills.",
            "Describe a challenging situation where you had to use {} effectively.",
            "Give me an example of how you've shown {} in your previous roles."
        ]

        # Use top behavioral skills
        for i, skill in enumerate(behav_skills[:3]):
            if i < len(behav_templates):
                questions.append({
                    "type": "behavioral",
                    "question": behav_templates[i].format(skill),
                    "target_competency": skill
                })

        # Technical questions (2)
        if tech_skills:
            tech_templates = [
                "Explain how you would implement a solution using {} in a production environment.",
                "Describe a challenging technical problem you solved using {}.",
                "How would you approach designing a system that utilizes {} and {}?"
            ]

            # Add technical questions based on available skills
            if len(tech_skills) >= 2:
                questions.append({
                    "type": "technical",
                    "question": tech_templates[2].format(tech_skills[0], tech_skills[1]),
                    "target_competency": tech_skills[0]
                })

            questions.append({
                "type": "technical",
                "question": tech_templates[0].format(tech_skills[0]),
                "target_competency": tech_skills[0]
            })

            questions.append({
                "type": "technical",
                "question": tech_templates[1].format(tech_skills[0]),
                "target_competency": tech_skills[0]
            })

        # Add job-specific questions based on keywords
        if "experience" in job_desc.lower():
            questions.append({
                "type": "behavioral",
                "question": "Walk me through your most significant professional achievement and your specific contributions.",
                "target_competency": "Experience & Impact"
            })

        if "team" in job_desc.lower():
            questions.append({
                "type": "behavioral",
                "question": "Tell me about a time when you had to work with a difficult team member or manage a conflict within your team.",
                "target_competency": "Teamwork & Conflict Resolution"
            })

        return questions

    def _define_success_metrics(self, questions: List[Dict[str, str]]) -> Dict[str, str]:
        """Define what constitutes successful answers for each question."""
        metrics = {}

        for i, q in enumerate(questions):
            question_key = f"question_{i}"
            if q["type"] == "behavioral":
                metrics[question_key] = (
                    "Should follow the STAR method (Situation, Task, Action, Result), "
                    "demonstrate specific examples with measurable outcomes, "
                    "and clearly show the candidate's individual contribution."
                )
            else:  # technical
                metrics[question_key] = (
                    "Should demonstrate technical depth, explain thought process, "
                    "consider edge cases, and show practical application of concepts."
                )

        return metrics