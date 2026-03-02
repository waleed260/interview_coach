"""
Basic tests for the AI Interview Coach system
"""
import pytest
from unittest.mock import Mock, patch
from interview_coach.agents.job_strategist import JobStrategist
from interview_coach.agents.interviewer import Interviewer
from interview_coach.agents.feedback_coach import FeedbackCoach


class TestJobStrategist:
    def test_analyze_basic_functionality(self):
        strategist = JobStrategist()

        job_desc = "Software Engineer position requiring Python, JavaScript, and AWS experience"
        resume = "I have 3 years of experience with Python and web development"

        strategy = strategist.analyze(job_desc, resume)

        assert "core_competencies" in strategy
        assert "predicted_questions" in strategy
        assert len(strategy["predicted_questions"]) > 0

    def test_extract_technical_skills(self):
        strategist = JobStrategist()

        job_desc = "We need someone with Python, JavaScript, AWS, Docker, and SQL experience"
        skills = strategist._extract_technical_skills(job_desc)

        assert len(skills) > 0
        # Check if at least some expected skills are found
        found_skills = [skill.lower() for skill in skills]
        expected_skills = ["python", "javascript", "aws", "docker", "sql"]

        assert any(exp.lower() in found_skills for exp in expected_skills)


class TestInterviewer:
    def test_ask_next_question(self):
        interviewer = Interviewer()

        strategy = {
            "predicted_questions": [
                {"type": "behavioral", "question": "Tell me about your experience with Python"},
                {"type": "technical", "question": "How would you optimize a Python function?"}
            ]
        }

        interviewer.set_strategy(strategy)

        first_q = interviewer.ask_next_question()
        assert "Python" in first_q

        second_q = interviewer.ask_next_question()
        assert "optimize" in second_q.lower() or "function" in second_q.lower()

    def test_session_completion(self):
        interviewer = Interviewer()

        strategy = {
            "predicted_questions": [{"type": "behavioral", "question": "Sample question"}]
        }

        interviewer.set_strategy(strategy)
        interviewer.ask_next_question()  # Ask the only question

        assert interviewer.is_session_complete()


class TestFeedbackCoach:
    def test_star_analysis(self):
        coach = FeedbackCoach()

        answer = "In my previous role, I was tasked with improving our API response times. The situation was that our users were experiencing slow load times. I analyzed the code and implemented caching mechanisms. As a result, we reduced response times by 40%."

        star_analysis = coach._analyze_star_method(answer)

        # Should identify most STAR components
        assert star_analysis["score"] >= 2  # At least 2 components should be found

    def test_clarity_assessment(self):
        coach = FeedbackCoach()

        answer = "Well, um, I had this situation where we needed to improve performance. So basically, I looked at the code and made it faster. The result was good."

        clarity = coach._assess_clarity(answer)

        # This answer should have low clarity due to fillers and lack of specifics
        assert clarity["filler_words"] > 0
        assert clarity["word_count"] < 100

    def test_process_answer(self):
        coach = FeedbackCoach()

        question = "Tell me about a time you solved a technical problem"
        answer = "I identified the issue, implemented a solution, and it worked well."

        coach.process_answer(question, answer, 0)

        assert 0 in coach.answer_evaluations
        evaluation = coach.answer_evaluations[0]
        assert "star_analysis" in evaluation
        assert "feedback" in evaluation