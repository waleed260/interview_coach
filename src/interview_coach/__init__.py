"""
AI Interview Coach Package

This package implements a multi-agent system for AI-powered interview coaching:
- Job Strategist: Analyzes job requirements and predicts questions
- Interviewer: Conducts mock interviews
- Feedback Coach: Provides evaluation and improvement suggestions
"""

from .system import InterviewCoachSystem


def main():
    """Entry point for the interview coach application."""
    coach_system = InterviewCoachSystem()
    coach_system.run()