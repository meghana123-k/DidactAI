from typing import List
from difflib import SequenceMatcher

from services.quiz_generator import (
    QuizQuestion,
    QuestionOption,
    DifficultyLevel
)


class QuizValidator:
    """
    Validates generated quiz questions and assigns a normalized difficulty score.
    """

    MIN_QUESTION_LENGTH = 10
    MIN_OPTIONS = 4

    def __init__(self):
        self._seen_questions = set()

    # ---------------- INTERNAL CHECKS ----------------

    def _is_duplicate(self, question_text: str) -> bool:
        normalized = question_text.lower().strip()
        if normalized in self._seen_questions:
            return True
        self._seen_questions.add(normalized)
        return False

    def _has_single_correct_option(self, options: List[QuestionOption]) -> bool:
        return sum(opt.is_correct for opt in options) == 1

    def _answer_leakage(self, question: QuizQuestion) -> bool:
        correct_text = next(
            opt.text.lower() for opt in question.options if opt.is_correct
        )
        question_text = question.question_text.lower()

        key_terms = [w for w in correct_text.split() if len(w) > 3]
        return any(term in question_text for term in key_terms)

    # ---------------- VALIDATION ----------------

    def is_valid(self, question: QuizQuestion) -> bool:
        if len(question.question_text.strip()) < self.MIN_QUESTION_LENGTH:
            return False

        if len(question.options) < self.MIN_OPTIONS:
            return False

        if not self._has_single_correct_option(question.options):
            return False

        if self._answer_leakage(question):
            return False

        if self._is_duplicate(question.question_text):
            return False

        return True

    # ---------------- DIFFICULTY SCORING ----------------

    def _option_similarity(self, options: List[QuestionOption]) -> float:
        texts = [opt.text.lower() for opt in options]
        similarities = []

        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                ratio = SequenceMatcher(None, texts[i], texts[j]).ratio()
                similarities.append(ratio)

        return sum(similarities) / len(similarities) if similarities else 0.0

    def _difficulty_score(self, question: QuizQuestion) -> float:
        """
        Returns difficulty score between 0.0 and 1.0
        """
        score = 0.0

        # 1️⃣ Question length (0–0.25)
        word_count = len(question.question_text.split())
        score += min(word_count / 40, 1.0) * 0.25

        # 2️⃣ Option similarity (0–0.35)
        score += self._option_similarity(question.options) * 0.35

        # 3️⃣ Cognitive level (0–0.25)
        level_weight = {
            DifficultyLevel.BEGINNER: 0.10,
            DifficultyLevel.INTERMEDIATE: 0.18,
            DifficultyLevel.ADVANCED: 0.25,
        }
        score += level_weight.get(question.difficulty_level, 0.15)

        # 4️⃣ Explanation presence (0–0.15)
        if question.explanation:
            score += 0.15

        return round(min(score, 1.0), 2)

    # ---------------- PUBLIC API ----------------

    def validate_and_score(
        self, questions: List[QuizQuestion]
    ) -> List[QuizQuestion]:
        """
        Filters invalid questions and assigns difficulty scores.
        """
        validated = []

        for q in questions:
            if not self.is_valid(q):
                continue

            q.difficulty_score = self._difficulty_score(q)
            validated.append(q)

        return validated
