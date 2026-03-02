"""
AI Interview Coach - Main Entry Point

This module orchestrates the multi-agent interview coaching system:
- Job Strategist: Analyzes job descriptions and resumes
- Interviewer: Conducts the mock interview
- Feedback Coach: Provides evaluation and suggestions
"""
import asyncio
from interview_coach.system import InterviewCoachSystem


def main():
    """Main entry point for the AI Interview Coach."""
    coach_system = InterviewCoachSystem()
    coach_system.run()


if __name__ == "__main__":
    main()