from datetime import datetime
from sqlalchemy.orm import Session
from models.certificate import Certificate


def create_or_update_certificate(
    db: Session,
    *,
    student_id: str,
    topic: str,
    accuracy: float,
    certificate_data: dict
) -> Certificate:
    """
    Highest-score-only certificate policy.

    - Creates certificate if none exists
    - Updates ONLY if new accuracy is higher
    """

    cert = (
        db.query(Certificate)
        .filter(
            Certificate.student_id == student_id,
            Certificate.topic == topic
        )
        .first()
    )

    # Case 1: First certificate
    if cert is None:
        cert = Certificate(
            student_id=student_id,
            topic=topic,
            best_accuracy=accuracy,
            certificate_data=certificate_data,
            certificate_version=1
        )
        db.add(cert)
        db.commit()
        db.refresh(cert)
        return cert

    # Case 2: Improved score → update
    if accuracy > float(cert.best_accuracy):
        cert.best_accuracy = accuracy
        cert.certificate_data = certificate_data
        cert.certificate_version += 1
        cert.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(cert)

    # Case 3: Worse or equal score → NO CHANGE
    return cert
