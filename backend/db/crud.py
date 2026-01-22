from sqlalchemy.orm import Session
from db.models import QuizAttempt, Certificate


# ------------------------------------------------
# QUIZ ATTEMPTS
# ------------------------------------------------
def save_quiz_attempt(db: Session, attempt_data: dict):
    attempt = QuizAttempt(**attempt_data)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


# ------------------------------------------------
# CERTIFICATES (Highest-Score Policy)
# ------------------------------------------------
def get_certificate(db: Session, student_id: str, topic: str):
    return (
        db.query(Certificate)
        .filter_by(student_id=student_id, topic=topic)
        .first()
    )


def create_or_update_certificate(
    db: Session,
    student_id: str,
    topic: str,
    accuracy: float,
    certificate_data: dict
):
    existing = get_certificate(db, student_id, topic)

    if existing:
        if accuracy > float(existing.best_accuracy):
            existing.best_accuracy = accuracy
            existing.certificate_data = certificate_data
            db.commit()
            db.refresh(existing)
            return existing, "updated"
        else:
            return existing, "unchanged"

    new_cert = Certificate(
        student_id=student_id,
        topic=topic,
        best_accuracy=accuracy,
        certificate_data=certificate_data
    )

    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return new_cert, "created"
