"""
Feedback Coach Agent - Evaluates responses and provides constructive feedback
"""
from typing import Dict, List, Any, Optional
import re


class FeedbackCoach:
    """Senior Career Coach agent that analyzes responses and provides feedback."""

    def __init__(self):
        self.strategy = None
        self.answer_evaluations = {}
        self.system_prompt = """
You are a Senior Career Coach. Your goal is to analyze the conversation transcript between the User and the Interviewer.

Evaluation Criteria:
- STAR Analysis: Did the user provide a clear Situation, Task, Action, and Result?
- Clarity & Conciseness: Is the answer too long or full of fluff?
- Gap Identification: Did they miss the core competency the Strategist identified?

Output: Provide a 'Constructive Critique' and a 'Better Answer' suggestion after every question.
"""

    def set_strategy(self, strategy: Dict[str, Any]):
        """Set the interview strategy from the Job Strategist."""
        self.strategy = strategy
        self.answer_evaluations = {}

    def process_answer(self, question: str, answer: str, answer_index: int):
        """Process and evaluate an answer in the background."""
        evaluation = self._evaluate_answer(question, answer)
        self.answer_evaluations[answer_index] = evaluation

    def _evaluate_answer(self, question: str, answer: str) -> Dict[str, Any]:
        """Evaluate a single answer using multiple criteria."""
        star_analysis = self._analyze_star_method(answer)
        clarity_score = self._assess_clarity(answer)
        competency_alignment = self._check_competency_alignment(question, answer)

        feedback = self._generate_feedback(star_analysis, clarity_score, competency_alignment, question, answer)
        improvement_suggestions = self._generate_improvement_suggestions(star_analysis, clarity_score, competency_alignment)

        return {
            "star_analysis": star_analysis,
            "clarity_score": clarity_score,
            "competency_alignment": competency_alignment,
            "feedback": feedback,
            "improvement_suggestions": improvement_suggestions
        }

    def _analyze_star_method(self, answer: str) -> Dict[str, Any]:
        """Analyze if the answer follows the STAR method."""
        answer_lower = answer.lower()

        # Look for STAR components
        situation_present = any(phrase in answer_lower for phrase in [
            "there was", "it happened", "at that time", "during", "when", "first", "initially"
        ])

        task_present = any(phrase in answer_lower for phrase in [
            "my role was", "i was responsible", "i had to", "the goal was", "we needed"
        ])

        action_present = any(phrase in answer_lower for phrase in [
            "i decided", "i implemented", "i worked", "i developed", "i collaborated",
            "so i", "then i", "next i", "first i", "after that"
        ])

        result_present = any(phrase in answer_lower for phrase in [
            "as a result", "this led to", "the outcome was", "we achieved", "finally",
            "ultimately", "the impact was", "which resulted in"
        ])

        star_components = {
            "situation": situation_present,
            "task": task_present,
            "action": action_present,
            "result": result_present
        }

        star_score = sum(star_components.values())
        star_status = f"{star_score}/4 STAR components identified"

        missing_components = [comp for comp, present in star_components.items() if not present]

        return {
            "components": star_components,
            "score": star_score,
            "status": star_status,
            "missing": missing_components
        }

    def _assess_clarity(self, answer: str) -> Dict[str, Any]:
        """Assess the clarity and conciseness of the answer."""
        word_count = len(answer.split())
        sentence_count = len([s for s in re.split(r'[.!?]+', answer) if s.strip()])
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        # Check for filler words
        filler_words = ["um", "uh", "well", "you know", "so", "basically", "actually", "like"]
        filler_count = sum(1 for word in filler_words if word in answer.lower())

        # Check for rambling indicators
        repetition_count = self._count_repetitions(answer)

        clarity_score = 10  # Base score

        # Deduct points for issues
        if word_count > 300:  # Too long
            clarity_score -= min((word_count - 300) // 50, 4)
        elif word_count < 30:  # Too short
            clarity_score -= 2

        if avg_sentence_length > 30:  # Sentences too long
            clarity_score -= 2

        if filler_count > 5:  # Too many fillers
            clarity_score -= min(filler_count // 2, 3)

        if repetition_count > 3:  # Too much repetition
            clarity_score -= min(repetition_count, 3)

        clarity_score = max(1, min(10, clarity_score))  # Clamp between 1-10

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "filler_words": filler_count,
            "repetition_count": repetition_count,
            "score": clarity_score,
            "rating": self._get_clarity_rating(clarity_score)
        }

    def _count_repetitions(self, text: str) -> int:
        """Count repetitive phrases in the text."""
        words = text.lower().split()
        word_counts = {}
        for word in words:
            word = re.sub(r'[^\w]', '', word)  # Remove punctuation
            if len(word) > 3:  # Ignore short words
                word_counts[word] = word_counts.get(word, 0) + 1

        # Count words that appear more than twice
        return sum(1 for count in word_counts.values() if count > 2)

    def _get_clarity_rating(self, score: int) -> str:
        """Convert clarity score to rating."""
        if score >= 8:
            return "Excellent"
        elif score >= 6:
            return "Good"
        elif score >= 4:
            return "Fair"
        else:
            return "Needs Improvement"

    def _check_competency_alignment(self, question: str, answer: str) -> Dict[str, Any]:
        """Check if the answer aligns with the targeted competency."""
        if not self.strategy:
            return {"aligned": False, "confidence": 0.0, "details": "No strategy loaded"}

        # Extract target competency from question or strategy
        target_competency = self._identify_target_competency(question)

        answer_lower = answer.lower()

        # Check if answer addresses the competency
        competency_mentioned = target_competency.lower() in answer_lower if target_competency else False

        # Look for related terms
        related_terms = self._get_related_terms(target_competency)
        related_mentioned = any(term.lower() in answer_lower for term in related_terms) if related_terms else False

        # Calculate alignment confidence
        confidence = 0.8 if competency_mentioned else (0.5 if related_mentioned else 0.2)

        return {
            "target_competency": target_competency,
            "aligned": competency_mentioned or related_mentioned,
            "confidence": confidence,
            "details": f"Mentions: {competency_mentioned}, Related: {related_mentioned}"
        }

    def _identify_target_competency(self, question: str) -> Optional[str]:
        """Identify the competency the question is targeting."""
        # Look in strategy for question match
        if self.strategy and "predicted_questions" in self.strategy:
            for q in self.strategy["predicted_questions"]:
                if q["question"] in question:
                    return q.get("target_competency", "")

        # Heuristic approach based on question content
        question_lower = question.lower()

        competency_indicators = {
            "Leadership": ["lead", "manage", "team", "direct", "supervise", "guide"],
            "Communication": ["communicate", "present", "explain", "convey", "articulate"],
            "Problem Solving": ["solve", "resolve", "address", "tackle", "overcome", "challenge"],
            "Technical Skills": ["implement", "develop", "build", "code", "design", "architecture"],
            "Adaptability": ["adapt", "adjust", "flexible", "change", "pivot", "evolve"],
            "Collaboration": ["collaborate", "work with", "partner", "coordinate", "cooperate"]
        }

        for competency, indicators in competency_indicators.items():
            if any(indicator in question_lower for indicator in indicators):
                return competency

        return "General"

    def _get_related_terms(self, competency: str) -> List[str]:
        """Get related terms for a competency."""
        related_map = {
            "Leadership": ["manage", "guide", "direct", "supervise", "influence", "motivate"],
            "Communication": ["express", "convey", "articulate", "present", "discuss", "share"],
            "Problem Solving": ["resolve", "tackle", "address", "overcome", "diagnose", "fix"],
            "Technical Skills": ["implement", "develop", "build", "engineer", "architect", "code"],
            "Adaptability": ["flexible", "adjust", "pivot", "accommodate", "embrace change"],
            "Collaboration": ["teamwork", "cooperate", "coordinate", "partnership", "synergy"]
        }

        return related_map.get(competency, [])

    def _generate_feedback(self, star_analysis: Dict, clarity: Dict, competency: Dict, question: str, answer: str) -> str:
        """Generate feedback based on all evaluations."""
        feedback_parts = []

        # STAR feedback
        if star_analysis["score"] < 3:
            missing = ", ".join(star_analysis["missing"])
            feedback_parts.append(f"Consider using the STAR method (Situation, Task, Action, Result). You missed: {missing}")

        # Clarity feedback
        if clarity["rating"] in ["Fair", "Needs Improvement"]:
            if clarity["filler_words"] > 3:
                feedback_parts.append(f"Avoid excessive filler words ({clarity['filler_words']} detected)")
            if clarity["word_count"] > 300:
                feedback_parts.append(f"Answer is quite long ({clarity['word_count']} words), consider being more concise")
            elif clarity["word_count"] < 50:
                feedback_parts.append(f"Answer is brief ({clarity['word_count']} words), add more specific details")

        # Competency feedback
        if not competency["aligned"]:
            feedback_parts.append(f"Your answer didn't clearly address the target competency: {competency['target_competency']}")

        if not feedback_parts:
            return "Strong answer! You addressed the key points effectively."
        else:
            return " ".join(feedback_parts)

    def _generate_improvement_suggestions(self, star_analysis: Dict, clarity: Dict, competency: Dict) -> List[str]:
        """Generate specific improvement suggestions."""
        suggestions = []

        if star_analysis["score"] < 4:
            suggestions.append("Structure your response using the STAR method (Situation, Task, Action, Result)")

        if clarity["filler_words"] > 3:
            suggestions.append("Practice speaking without filler words like 'um', 'uh', 'well'")

        if clarity["avg_sentence_length"] > 25:
            suggestions.append("Break down long sentences for better clarity")

        if not competency["aligned"]:
            suggestions.append(f"Make sure to directly address the competency: {competency['target_competency']}")

        if star_analysis["missing"]:
            missing = ", ".join([item.title() for item in star_analysis["missing"]])
            suggestions.append(f"Include more details about: {missing}")

        return suggestions

    def provide_interim_feedback(self, conversation_history: List[Dict]) -> str:
        """Provide feedback on the entire conversation so far."""
        if not conversation_history:
            return "No responses to evaluate yet. Please answer at least one question."

        last_exchange = conversation_history[-1]
        answer_idx = len(conversation_history) - 1

        if answer_idx in self.answer_evaluations:
            eval_result = self.answer_evaluations[answer_idx]

            feedback_text = f"Feedback on your response:\n\n"
            feedback_text += f"STAR Method: {eval_result['star_analysis']['status']}\n"
            feedback_text += f"Clarity Score: {eval_result['clarity_score']['score']}/10 ({eval_result['clarity_score']['rating']})\n"
            feedback_text += f"Competency Alignment: {'✓' if eval_result['competency_alignment']['aligned'] else '✗'}\n\n"
            feedback_text += f"Evaluation: {eval_result['feedback']}\n\n"

            if eval_result['improvement_suggestions']:
                feedback_text += "Suggestions for improvement:\n"
                for i, suggestion in enumerate(eval_result['improvement_suggestions'], 1):
                    feedback_text += f"{i}. {suggestion}\n"

            return feedback_text
        else:
            return "Processing your response... Please wait for feedback."

    def generate_final_summary(self, conversation_history: List[Dict]) -> str:
        """Generate a final feedback summary after the interview."""
        if not conversation_history:
            return "No interview conducted. No feedback to provide."

        # Calculate overall statistics
        total_answers = len(conversation_history)
        avg_star_score = 0
        avg_clarity_score = 0
        aligned_answers = 0

        for i, exchange in enumerate(conversation_history):
            if i in self.answer_evaluations:
                eval_result = self.answer_evaluations[i]
                avg_star_score += eval_result['star_analysis']['score']
                avg_clarity_score += eval_result['clarity_score']['score']

                if eval_result['competency_alignment']['aligned']:
                    aligned_answers += 1

        if total_answers > 0:
            avg_star_score /= total_answers
            avg_clarity_score /= total_answers
            alignment_rate = (aligned_answers / total_answers) * 100
        else:
            avg_star_score = avg_clarity_score = alignment_rate = 0

        summary = f"Interview Performance Summary:\n"
        summary += f"- Total Questions Answered: {total_answers}\n"
        summary += f"- Average STAR Score: {avg_star_score:.1f}/4\n"
        summary += f"- Average Clarity Score: {avg_clarity_score:.1f}/10\n"
        summary += f"- Competency Alignment Rate: {alignment_rate:.1f}%\n\n"

        # Strengths
        strengths = []
        if avg_clarity_score >= 7:
            strengths.append("Strong communication and clarity")
        if avg_star_score >= 2.5:
            strengths.append("Good use of STAR method")
        if alignment_rate >= 70:
            strengths.append("Good alignment with job requirements")

        if strengths:
            summary += f"Key Strengths:\n"
            for strength in strengths:
                summary += f"- {strength}\n"
        else:
            summary += "Key Strengths: Could not identify clear strengths. Review recommendations below.\n"

        # Areas for improvement
        summary += f"\nAreas for Improvement:\n"

        if avg_clarity_score < 7:
            summary += "- Work on delivering clearer, more concise responses\n"
        if avg_star_score < 2.5:
            summary += "- Practice structuring answers with the STAR method\n"
        if alignment_rate < 70:
            summary += "- Better align your responses with the job requirements\n"

        # Individual feedback
        summary += f"\nDetailed Feedback:\n"
        for i, exchange in enumerate(conversation_history):
            if i in self.answer_evaluations:
                eval_result = self.answer_evaluations[i]
                summary += f"\nQ{i+1}: {exchange['question'][:60]}...\n"
                summary += f"   Feedback: {eval_result['feedback'][:80]}...\n"
                if eval_result['improvement_suggestions']:
                    summary += f"   Tip: {eval_result['improvement_suggestions'][0]}\n"

        return summary