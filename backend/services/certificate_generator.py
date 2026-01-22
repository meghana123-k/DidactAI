from typing import Dict, Optional
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
CERTIFICATE_PASS_THRESHOLD = 80.0  # % accuracy


# ============================================================
# CORE CERTIFICATE LOGIC
# ============================================================
def create_or_update_certificate(
    student_id: str,
    topic: str,
    analytics: Dict,
    existing_certificate: Optional[Dict] = None
) -> Dict:
    """
    Highest-score-only certificate policy.

    Parameters:
    - student_id: learner identifier
    - topic: subject/topic name
    - analytics: output from analytics_engine.py
    - existing_certificate: persisted certificate data (if any)

    Returns:
    - certificate decision payload (DB-ready)
    """

    overall = analytics.get("overall", {})
    post_accuracy = float(overall.get("post_accuracy", 0))

    # --------------------------------------------------------
    # Eligibility check
    # --------------------------------------------------------
    if post_accuracy < CERTIFICATE_PASS_THRESHOLD:
        return {
            "issued": False,
            "action": "rejected",
            "reason": "Score below certification threshold",
            "best_accuracy": (
                existing_certificate["best_accuracy"]
                if existing_certificate
                else None
            )
        }

    # --------------------------------------------------------
    # First-time certificate
    # --------------------------------------------------------
    if existing_certificate is None:
        return {
            "issued": True,
            "action": "new",
            "student_id": student_id,
            "topic": topic,
            "best_accuracy": post_accuracy,
            "certificate_version": 1,
            "certificate_data": {
                "topic": topic,
                "accuracy": post_accuracy,
                "issued_at": datetime.utcnow().isoformat()
            }
        }

    # --------------------------------------------------------
    # Highest-score-only update
    # --------------------------------------------------------
    previous_best = float(existing_certificate["best_accuracy"])

    if post_accuracy > previous_best:
        return {
            "issued": True,
            "action": "update",
            "student_id": student_id,
            "topic": topic,
            "best_accuracy": post_accuracy,
            "certificate_version": existing_certificate["certificate_version"] + 1,
            "certificate_data": {
                **existing_certificate["certificate_data"],
                "accuracy": post_accuracy,
                "updated_at": datetime.utcnow().isoformat()
            }
        }

    # --------------------------------------------------------
    # No update needed
    # --------------------------------------------------------
    return {
        "issued": False,
        "action": "unchanged",
        "best_accuracy": previous_best,
        "reason": "Existing certificate has higher or equal score"
    }
