from dataclasses import dataclass
from typing import List
import math


@dataclass
class QuestionBehavior:
    """
    Behavioral data collected per question.
    """
    question_id: int
    time_spent: float        # seconds spent answering
    idle_time: float         # seconds idle during this question
    tab_switches: int        # tab switches during this question


class IntegrityMonitor:
    """
    Computes integrity score using non-intrusive behavioral analytics.
    """

    def __init__(self):
        # Weight distribution (sum = 1.0)
        self.weights = {
            "tab_switch": 0.40,
            "idle_time": 0.20,
            "fast_answer": 0.25,
            "timing_variance": 0.15
        }

        # Thresholds (empirically chosen, explainable)
        self.thresholds = {
            "fast_answer_sec": 8.0,        # answers faster than this are suspicious
            "tab_switch_limit": 4,         # acceptable tab switches per quiz
            "max_idle_sec": 45.0,           # idle time beyond this is suspicious
            "min_std_dev_sec": 4.0,         # too-uniform answering
            "normal_std_dev_ref": 12.0      # expected natural variation
        }

    # ─────────────────────────────────────────────
    # Suspicion Component Scores
    # ─────────────────────────────────────────────

    def _tab_switch_score(self, behaviors: List[QuestionBehavior]) -> float:
        total_switches = sum(b.tab_switches for b in behaviors)
        excess_ratio = total_switches / (self.thresholds["tab_switch_limit"] + 2)
        return min(1.0, excess_ratio)

    def _idle_time_score(self, behaviors: List[QuestionBehavior]) -> float:
        idle_violations = sum(
            1 for b in behaviors if b.idle_time > self.thresholds["max_idle_sec"]
        )
        return idle_violations / len(behaviors)

    def _fast_answer_score(self, behaviors: List[QuestionBehavior]) -> float:
        fast_answers = sum(
            1 for b in behaviors if b.time_spent < self.thresholds["fast_answer_sec"]
        )
        fast_ratio = fast_answers / len(behaviors)
        return min(1.0, fast_ratio * 2)

    def _timing_variance_score(self, behaviors: List[QuestionBehavior]) -> float:
        times = [b.time_spent for b in behaviors]
        if len(times) < 3:
            return 0.0

        mean = sum(times) / len(times)
        variance = sum((t - mean) ** 2 for t in times) / len(times)
        std_dev = math.sqrt(variance)

        if std_dev >= self.thresholds["min_std_dev_sec"]:
            return 0.0

        penalty = 1 - (std_dev / self.thresholds["normal_std_dev_ref"])
        return min(1.0, max(0.0, penalty))

    # ─────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────

    def compute_integrity_score(self, behaviors: List[QuestionBehavior]) -> dict:
        """
        Returns integrity score, suspicion score, category, and breakdown.
        """

        if not behaviors:
            return {
                "integrity_score": 1.0,
                "suspicion_score": 0.0,
                "category": "Normal",
                "details": {}
            }

        suspicion = (
            self._tab_switch_score(behaviors) * self.weights["tab_switch"] +
            self._idle_time_score(behaviors) * self.weights["idle_time"] +
            self._fast_answer_score(behaviors) * self.weights["fast_answer"] +
            self._timing_variance_score(behaviors) * self.weights["timing_variance"]
        )

        suspicion = round(min(1.0, suspicion), 3)
        integrity = round(1.0 - suspicion, 3)

        category = (
            "Normal" if integrity >= 0.80 else
            "Warning" if integrity >= 0.60 else
            "Flagged"
        )

        return {
            "integrity_score": integrity,
            "suspicion_score": suspicion,
            "category": category,
            "details": {
                "total_questions": len(behaviors),
                "tab_switches": sum(b.tab_switches for b in behaviors),
                "fast_answers": sum(
                    1 for b in behaviors if b.time_spent < self.thresholds["fast_answer_sec"]
                ),
                "high_idle_questions": sum(
                    1 for b in behaviors if b.idle_time > self.thresholds["max_idle_sec"]
                )
            }
        }
