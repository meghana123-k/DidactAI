from sqlalchemy.orm import Session
from models.quiz_attempt import QuizAttempt


def save_quiz_attempt(db: Session, attempt_payload: dict) -> QuizAttempt:
    """
    Persists a quiz attempt (pre or post).

    Expected payload keys (STRICT):
    - student_id
    - topic
    - assessment_phase  ('pre' | 'post')
    - summary_mode      ('basic' | 'conceptual' | 'detailed')
    - accuracy
    - total_score
    - max_score
    - difficulty_analysis
    - concept_analysis
    - attempt_metadata (optional)
    - integrity_score  (optional)
    """

    attempt = QuizAttempt(
        student_id=attempt_payload["student_id"],
        topic=attempt_payload["topic"],
        assessment_phase=attempt_payload["assessment_phase"],
        summary_mode=attempt_payload["summary_mode"],
        accuracy=attempt_payload["accuracy"],
        total_score=attempt_payload["total_score"],
        max_score=attempt_payload["max_score"],
        difficulty_analysis=attempt_payload["difficulty_analysis"],
        concept_analysis=attempt_payload["concept_analysis"],
        attempt_metadata=attempt_payload.get("attempt_metadata"),
        integrity_score=attempt_payload.get("integrity_score"),
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt
