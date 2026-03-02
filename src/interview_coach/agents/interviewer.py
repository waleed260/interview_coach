"""
Interviewer Agent - Conducts the mock interview
"""
from typing import Dict, List, Any, Optional


class Interviewer:
    """Professional interviewer agent that conducts realistic mock interviews."""

    def __init__(self):
        self.strategy = None
        self.current_question_index = 0
        self.responses_received = []
        self.system_prompt = """
You are a professional Interviewer for [Target Company/Industry]. Your goal is to conduct a realistic mock interview.

Instructions:
- Ask one question at a time. Do not give feedback during the session.
- Stay in character: Be polite but professional. If the user gives a weak answer, press them for more detail (e.g., 'Can you elaborate on your specific contribution to that project?').
- Adaptivity: Use the core competencies identified by the Strategist to tailor your questions.
- End criteria: Once all planned questions are exhausted, notify the user that the interview is concluded.
"""

    def set_strategy(self, strategy: Dict[str, Any]):
        """Set the interview strategy from the Job Strategist."""
        self.strategy = strategy
        self.current_question_index = 0
        self.responses_received = []

    def ask_next_question(self) -> Optional[str]:
        """Ask the next question in sequence."""
        if not self.strategy:
            return "Interviewer: No strategy loaded. Please initialize with job requirements first."

        questions = self.strategy.get("predicted_questions", [])

        if self.current_question_index >= len(questions):
            return None  # No more questions

        current_question = questions[self.current_question_index]
        self.current_question_index += 1

        return current_question["question"]

    def record_response(self, response: str):
        """Record the user's response to the current question."""
        if len(self.responses_received) < self.current_question_index:
            self.responses_received.append(response)
        else:
            # Update existing response if user is revising
            self.responses_received[-1] = response

    def is_session_complete(self) -> bool:
        """Check if all questions have been asked and answered."""
        if not self.strategy:
            return True

        questions = self.strategy.get("predicted_questions", [])
        return self.current_question_index >= len(questions)

    def follow_up_on_weak_answer(self, response: str) -> str:
        """Generate a follow-up question if the answer seems weak."""
        weak_indicators = [
            "um", "uh", "well", "you know", "kind of", "sort of",
            "not sure", "maybe", "probably", "i think"
        ]

        response_lower = response.lower()
        has_weak_indicators = any(indicator in response_lower for indicator in weak_indicators)

        # Check for vagueness
        vague_indicators = [
            "stuff", "things", "some", "various", "different",
            "pretty much", "basically", "just"
        ]

        has_vague_indicators = any(indicator in response_lower for indicator in vague_indicators)

        if has_weak_indicators or has_vague_indicators or len(response.split()) < 10:
            follow_ups = [
                "Can you elaborate on your specific contribution to that project?",
                "Could you provide a more concrete example?",
                "What were the measurable results of your actions?",
                "Can you walk me through the steps you took?",
                "How did your specific actions lead to that outcome?"
            ]

            # Return an appropriate follow-up based on context
            return follow_ups[len(self.responses_received) % len(follow_ups)]

        return ""

    def get_remaining_questions_count(self) -> int:
        """Get the number of remaining questions."""
        if not self.strategy:
            return 0

        questions = self.strategy.get("predicted_questions", [])
        return max(0, len(questions) - self.current_question_index)