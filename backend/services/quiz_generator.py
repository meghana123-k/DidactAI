from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import random
import re


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class QuestionOption:
    text: str
    is_correct: bool


@dataclass
class QuizQuestion:
    question_text: str
    options: List[QuestionOption]
    difficulty_level: DifficultyLevel
    explanation: Optional[str] = None


class QuizGenerator:
    """Generates deterministic MCQ quizzes from summarized and conceptual content."""

    def _build_options(self, correct: str, distractors: List[str]) -> List[QuestionOption]:
        distractors = [d for d in distractors if d.lower() != correct.lower()]
        distractors = distractors[:3]

        options = [QuestionOption(correct, True)]
        options += [QuestionOption(d, False) for d in distractors]

        random.shuffle(options)
        return options

    # ---------------- BEGINNER ----------------
    def generate_beginner_questions(
        self, summary: str, key_terms: List[str]
    ) -> List[QuizQuestion]:
        questions = []
        sentences = re.split(r'(?<=[.!?])\s+', summary)

        for sentence in sentences:
            for term in key_terms:
                if term.lower() in sentence.lower():
                    masked = re.sub(
                        term, "______", sentence, flags=re.IGNORECASE
                    )
                    options = self._build_options(
                        correct=term,
                        distractors=key_terms
                    )

                    questions.append(
                        QuizQuestion(
                            question_text=masked,
                            options=options,
                            difficulty_level=DifficultyLevel.BEGINNER,
                            explanation=f"The correct answer is '{term}', as stated in the summary."
                        )
                    )
                    break

            if len(questions) >= 5:
                break

        return questions

    # ---------------- INTERMEDIATE ----------------
    def generate_intermediate_questions(
        self, concepts: List[str], concept_definitions: Dict[str, str]
    ) -> List[QuizQuestion]:
        questions = []

        for concept in concepts[:5]:
            question_text = f"What best describes the concept of {concept}?"

            correct_def = concept_definitions.get(
                concept, f"{concept} is a key concept related to this topic."
            )

            distractors = [
                d for c, d in concept_definitions.items()
                if c.lower() != concept.lower()
            ]

            options = self._build_options(correct_def, distractors)

            questions.append(
                QuizQuestion(
                    question_text=question_text,
                    options=options,
                    difficulty_level=DifficultyLevel.INTERMEDIATE,
                    explanation=f"{concept} refers to its role or meaning within the topic."
                )
            )

        return questions

    # ---------------- ADVANCED ----------------
    def generate_advanced_questions(
        self, relationships: List[Dict[str, str]]
    ) -> List[QuizQuestion]:
        questions = []

        for rel in relationships[:5]:
            subject = rel.get("subject")
            verb = rel.get("verb")
            obj = rel.get("object")

            if not subject or not verb or not obj:
                continue

            question_text = f"Who {verb} {obj}?"

            options = self._build_options(
                correct=subject,
                distractors=[obj, verb, "None of the above"]
            )

            questions.append(
                QuizQuestion(
                    question_text=question_text,
                    options=options,
                    difficulty_level=DifficultyLevel.ADVANCED,
                    explanation=f"The relationship shows that {subject} {verb} {obj}."
                )
            )

        return questions

    # ---------------- FULL QUIZ ----------------
    def generate_quiz(
        self,
        summary: str,
        concepts: List[str],
        key_terms: List[str],
        relationships: List[Dict[str, str]],
        concept_definitions: Optional[Dict[str, str]] = None
    ) -> Dict[DifficultyLevel, List[QuizQuestion]]:

        return {
            DifficultyLevel.BEGINNER: self.generate_beginner_questions(
                summary, key_terms
            ),
            DifficultyLevel.INTERMEDIATE: self.generate_intermediate_questions(
                concepts, concept_definitions or {}
            ),
            DifficultyLevel.ADVANCED: self.generate_advanced_questions(
                relationships
            ),
        },
        