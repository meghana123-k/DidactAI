from typing import Dict
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

# Minimum accuracy required to unlock next level
UNLOCK_THRESHOLDS = {
    "beginner": 60,
    "intermediate": 60,
    "advanced": 0   # no unlock after advanced
}

# Order is IMPORTANT
DIFFICULTY_ORDER = ["beginner", "intermediate", "advanced"]


# ============================================================
# CORE ENGINE
# ============================================================

def evaluate_difficulty_progression(
    analytics_result: Dict
) -> Dict:
    """
    Determines difficulty progression based on analytics output.

    Input:
    - analytics_result (from analytics_engine.analyze_quiz_performance)

    Output:
    - unlocked_levels
    - next_recommended_level
    - repeat_level (if any)
    """

    difficulty_readiness = analytics_result.get("difficulty_readiness", {})
    passed = analytics_result.get("passed", False)

    unlocked = []
    repeat_level = None
    next_level = None

    # --------------------------------------------------------
    # STEP 1: Determine unlocked levels
    # --------------------------------------------------------
    for level in DIFFICULTY_ORDER:
        stats = difficulty_readiness.get(level, {})
        accuracy = stats.get("accuracy", 0)

        if accuracy >= UNLOCK_THRESHOLDS[level]:
            unlocked.append(level)
        else:
            repeat_level = level
            break

    # --------------------------------------------------------
    # STEP 2: Determine next recommended level
    # --------------------------------------------------------
    if repeat_level:
        next_level = repeat_level
    else:
        if len(unlocked) < len(DIFFICULTY_ORDER):
            next_level = DIFFICULTY_ORDER[len(unlocked)]
        else:
            next_level = "completed"

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------
    return {
        "timestamp": datetime.utcnow().isoformat(),

        "unlocked_levels": unlocked,
        "repeat_level": repeat_level,
        "next_recommended_level": next_level,

        "can_attempt_advanced": "advanced" in unlocked,
        "status": _status_label(passed, next_level)
    }


# ============================================================
# HELPERS
# ============================================================

def _status_label(passed: bool, next_level: str) -> str:
    if next_level == "completed":
        return "course_completed"
    if not passed:
        return "retry_required"
    return "progressing"
