# services/quiz_validator.py
from typing import Dict
from datetime import datetime


def validate_quiz_attempt(
    quiz: Dict,
    user_answers: Dict[str, str],
    attempt_metadata: Dict[str, Dict] | None = None
) -> Dict:
    """
    PURE VALIDATOR.
    - Checks answers
    - Produces raw correctness facts
    - NO scoring
    - NO analytics
    """

    attempt_metadata = attempt_metadata or {}

    # Normalize quiz structure
    quiz_data = quiz["quiz"] if "quiz" in quiz else quiz

    detailed_results = []

    for level, questions in quiz_data.items():
        for idx, q in enumerate(questions):
            question_id = f"{level}_{idx}"
            selected = user_answers.get(question_id)
            correct = q["answer"]

            is_correct = selected == correct

            detailed_results.append({
                "question_id": question_id,
                "difficulty": q["difficulty"],
                "concept": correct,  # atomic concept
                "selected": selected,
                "correct_answer": correct,
                "is_correct": is_correct,
                "time_taken": attempt_metadata.get(question_id, {}).get("time_taken"),
                "timestamp": datetime.utcnow().isoformat()
            })

    return {
        "results": detailed_results
    }
