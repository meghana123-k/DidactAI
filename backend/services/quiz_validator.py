from typing import Dict
from datetime import datetime


def validate_quiz_attempt(
    quiz: Dict,
    user_answers: Dict[str, str],
    attempt_metadata: Dict[str, Dict] | None = None
) -> Dict:
    """
    Validates answers and produces raw correctness facts.
    NO scoring. NO pass/fail. NO analytics.
    """

    attempt_metadata = attempt_metadata or {}

    # ✅ Normalize quiz structure
    quiz_data = quiz["quiz"] if "quiz" in quiz else quiz

    results = []
    concept_events = []

    for level, questions in quiz_data.items():
        for idx, q in enumerate(questions):
            question_id = f"{level}_{idx}"
            selected = user_answers.get(question_id)
            correct = q["answer"]

            is_correct = selected == correct

            results.append({
                "question_id": question_id,
                "difficulty": q["difficulty"],
                "concept": correct,
                "selected": selected,
                "correct_answer": correct,
                "is_correct": is_correct,
                "timestamp": datetime.utcnow().isoformat(),
                "time_taken": attempt_metadata.get(question_id, {}).get("time_taken")
            })

            concept_events.append({
                "concept": correct,
                "difficulty": q["difficulty"],
                "is_correct": is_correct
            })

    return {
        "results": results,
        "concept_events": concept_events
    }
