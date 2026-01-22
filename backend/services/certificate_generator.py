from typing import Dict, Optional
from datetime import datetime
import uuid

# ============================================================
# CONFIGURATION
# ============================================================
CERTIFICATE_THRESHOLD = 80  # % accuracy required to certify


# ============================================================
# CORE CERTIFICATE LOGIC
# ============================================================
def generate_or_update_certificate(
    student_id: str,
    topic: str,
    analytics: Dict,
    previous_certificate: Optional[Dict] = None
) -> Dict:
    """
    Highest-score certificate policy.

    Rules:
    - Certificate issued only if accuracy >= CERTIFICATE_THRESHOLD
    - Certificate updated ONLY if current accuracy > previous best
    - Minor improvements below threshold are ignored
    """

    # ------------------------
    # Input validation
    # ------------------------
    if "summary" not in analytics:
        raise ValueError("Invalid analytics object: missing summary")

    current_accuracy = analytics["summary"].get("accuracy")

    if current_accuracy is None:
        raise ValueError("Analytics summary missing accuracy")

    if current_accuracy < CERTIFICATE_THRESHOLD:
        return {
            "eligible": False,
            "reason": "Accuracy below certification threshold",
            "current_accuracy": current_accuracy,
        }

    # ------------------------
    # First-time certificate
    # ------------------------
    if previous_certificate is None:
        return _create_certificate(
            student_id=student_id,
            topic=topic,
            accuracy=current_accuracy,
            analytics=analytics,
            is_update=False
        )

    # ------------------------
    # Compare with best score
    # ------------------------
    previous_best = previous_certificate.get("accuracy", 0)

    if current_accuracy <= previous_best:
        return {
            "eligible": False,
            "reason": "No improvement over existing certificate",
            "current_accuracy": current_accuracy,
            "best_accuracy": previous_best,
            "certificate_id": previous_certificate.get("certificate_id")
        }

    # ------------------------
    # Update certificate (higher mastery achieved)
    # ------------------------
    return _create_certificate(
        student_id=student_id,
        topic=topic,
        accuracy=current_accuracy,
        analytics=analytics,
        is_update=True,
        previous_certificate_id=previous_certificate.get("certificate_id")
    )


# ============================================================
# INTERNAL HELPERS
# ============================================================
def _create_certificate(
    student_id: str,
    topic: str,
    accuracy: float,
    analytics: Dict,
    is_update: bool,
    previous_certificate_id: Optional[str] = None
) -> Dict:
    """
    Creates a certificate metadata object.
    """

    certificate_id = str(uuid.uuid4())

    return {
        "eligible": True,
        "certificate": {
            "certificate_id": certificate_id,
            "student_id": student_id,
            "topic": topic,
            "accuracy": accuracy,
            "issued_at": datetime.utcnow().isoformat(),
            "is_update": is_update,
            "previous_certificate_id": previous_certificate_id,
            "mastery_snapshot": {
                "difficulty_progress": analytics.get("difficulty_progress", {}),
                "concept_progress": analytics.get("concept_progress", {}),
            }
        }
    }
