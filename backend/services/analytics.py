from typing import List, Dict
from backend.services.quiz_generator import QuizQuestion, DifficultyLevel


class AnalyticsEngine:
    """
    Computes performance metrics and learning gain.
    """

    def _accuracy(self, questions: List[QuizQuestion]) -> float:
        correct = sum(
            1 for q in questions
            if any(opt.is_correct and opt.text == q.selected_option for opt in q.options)
        )
        return correct / len(questions) if questions else 0.0

    def _weighted_score(self, questions: List[QuizQuestion]) -> float:
        total_weight = 0.0
        weighted_correct = 0.0

        for q in questions:
            weight = getattr(q, "difficulty_score", 1.0)
            total_weight += weight

            if any(opt.is_correct and opt.text == q.selected_option for opt in q.options):
                weighted_correct += weight

        return weighted_correct / total_weight if total_weight else 0.0

    def compute_metrics(
        self,
        questions: List[QuizQuestion],
        integrity_score: float,
        baseline_score: float = None
    ) -> Dict:

        accuracy = round(self._accuracy(questions), 3)
        weighted = round(self._weighted_score(questions), 3)
        final_score = round(weighted * integrity_score, 3)

        learning_gain = None
        if baseline_score is not None:
            learning_gain = round(final_score - baseline_score, 3)

        breakdown = {}
        for level in DifficultyLevel:
            level_qs = [q for q in questions if q.difficulty_level == level]
            breakdown[level.value] = {
                "accuracy": round(self._accuracy(level_qs), 3),
                "count": len(level_qs)
            }

        return {
            "accuracy": accuracy,
            "weighted_score": weighted,
            "integrity_score": round(integrity_score, 3),
            "final_score": final_score,
            "learning_gain": learning_gain,
            "breakdown": breakdown
        }
