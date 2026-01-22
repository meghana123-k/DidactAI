from typing import Dict, Optional
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
CERTIFICATE_PASS_THRESHOLD = 80  # % accuracy


# ============================================================
# CORE CERTIFICATE LOGIC
# ============================================================
def create_or_update_certificate(
    user_id: str,
    analytics: Dict,
    existing_certificate: Optional[Dict] = None
) -> Dict:
    """
    Highest-score-only certificate policy.

    Parameters:
    - user_id: unique learner identifier
    - analytics: output from analytics_engine.py
    - existing_certificate: previously issued certificate (if any)

    Returns:
    - certificate payload (issued or unchanged)
    """

    overall = analytics.get("overall", {})
    accuracy = overall.get("post_accuracy", 0)

    # --------------------------------------------------------
    # Eligibility check
    # --------------------------------------------------------
    if accuracy < CERTIFICATE_PASS_THRESHOLD:
        return {
            "issued": False,
            "reason": "Score below certification threshold",
            "best_score": existing_certificate.get("score") if existing_certificate else None
        }

    # --------------------------------------------------------
    # First-time certificate
    # --------------------------------------------------------
    if existing_certificate is None:
        return _issue_new_certificate(user_id, accuracy)

    # --------------------------------------------------------
    # Highest-score-only update
    # --------------------------------------------------------
    previous_best = existing_certificate.get("score", 0)

    if accuracy > previous_best:
        return _update_certificate(existing_certificate, accuracy)

    # --------------------------------------------------------
    # No update needed
    # --------------------------------------------------------
    return {
        "issued": False,
        "reason": "Existing certificate has higher or equal score",
        "best_score": previous_best
    }


# ============================================================
# HELPERS
# ============================================================
def _issue_new_certificate(user_id: str, score: float) -> Dict:
    return {
        "issued": True,
        "user_id": user_id,
        "score": score,
        "issued_at": datetime.utcnow().isoformat(),
        "certificate_version": 1,
        "status": "active"
    }


def _update_certificate(existing_certificate: Dict, new_score: float) -> Dict:
    return {
        **existing_certificate,
        "issued": True,
        "score": new_score,
        "updated_at": datetime.utcnow().isoformat(),
        "certificate_version": existing_certificate.get("certificate_version", 1) + 1,
        "status": "updated"
    }
