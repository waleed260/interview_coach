"""
Interview Coach System - Orchestrates the multi-agent interview coaching system
"""
import asyncio
from typing import Dict, Any, Optional
from .agents.job_strategist import JobStrategist
from .agents.interviewer import Interviewer
from .agents.feedback_coach import FeedbackCoach
from .utils import validate_job_description, validate_resume, sanitize_input


class InterviewCoachSystem:
    """Main system that coordinates the three AI agents for interview coaching."""

    def __init__(self):
        self.job_strategist = JobStrategist()
        self.interviewer = Interviewer()
        self.feedback_coach = FeedbackCoach()
        self.conversation_history = []

    def run(self):
        """Run the main interview coaching workflow."""
        print("Welcome to AI Interview Coach!")
        print("=" * 50)
        print("This system will help you prepare for your upcoming interview.")
        print("Please provide the following information:\n")

        # Get job description and resume from user
        while True:
            print("Please provide the job description:")
            job_description = input("> ")
            job_description = sanitize_input(job_description)

            is_valid, error_msg = validate_job_description(job_description)
            if is_valid:
                break
            else:
                print(f"Error: {error_msg}\nPlease try again.")

        while True:
            print("\nPlease provide your resume/CV:")
            resume = input("> ")
            resume = sanitize_input(resume)

            is_valid, error_msg = validate_resume(resume)
            if is_valid:
                break
            else:
                print(f"Error: {error_msg}\nPlease try again.")

        # Generate interview strategy
        print("\nAnalyzing job requirements and preparing interview...")
        try:
            strategy = self.job_strategist.analyze(job_description, resume)
        except Exception as e:
            print(f"Error analyzing job description and resume: {str(e)}")
            return

        # Initialize interviewer with strategy
        self.interviewer.set_strategy(strategy)
        self.feedback_coach.set_strategy(strategy)

        print(f"\nInterview preparation complete!")
        print(f"Expected questions: {len(strategy.get('predicted_questions', []))}")
        print("\nStarting mock interview. Type 'quit' to end early, 'feedback' for analysis.\n")

        # Start the interview loop
        self._interview_loop()

        # Final feedback
        print("\n" + "=" * 50)
        print("FINAL FEEDBACK SUMMARY")
        print("=" * 50)
        try:
            final_feedback = self.feedback_coach.generate_final_summary(self.conversation_history)
            print(final_feedback)
        except Exception as e:
            print(f"Error generating final feedback: {str(e)}")

    def _interview_loop(self):
        """Main interview interaction loop."""
        while True:
            try:
                # Interviewer asks a question
                question = self.interviewer.ask_next_question()

                if not question or self.interviewer.is_session_complete():
                    print("\nInterviewer: That concludes our mock interview. Thank you for participating!")
                    break

                print(f"\nInterviewer: {question}")

                # Get user response
                user_response = input("\nYou: ")

                if user_response.lower().strip() in ['quit', 'exit', 'q']:
                    print("\nInterview terminated by user.")
                    break
                elif user_response.lower().strip() == 'feedback':
                    # Show interim feedback
                    try:
                        feedback = self.feedback_coach.provide_interim_feedback(self.conversation_history)
                        print(f"\nFeedback Coach: {feedback}")
                    except Exception as e:
                        print(f"\nFeedback Coach: Error generating feedback: {str(e)}")
                    continue

                # Record the exchange
                exchange = {
                    "question": question,
                    "answer": user_response,
                    "timestamp": len(self.conversation_history)
                }
                self.conversation_history.append(exchange)

                # Provide immediate feedback in background (silently)
                try:
                    self.feedback_coach.process_answer(question, user_response, len(self.conversation_history)-1)
                except Exception as e:
                    print(f"[Debug: Error processing answer: {str(e)}]")

                # Move to next question
                self.interviewer.record_response(user_response)

            except KeyboardInterrupt:
                print("\n\nInterview interrupted by user.")
                break
            except Exception as e:
                print(f"\nAn error occurred during the interview: {str(e)}")
                print("Continuing interview...")

    def get_conversation_history(self) -> list:
        """Return the conversation history."""
        return self.conversation_history