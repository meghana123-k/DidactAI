from typing import Dict, List

# ============================================================
# CONFIG
# ============================================================
ORDERED_LEVELS = ["beginner", "intermediate", "advanced"]


# ============================================================
# CORE LOGIC
# ============================================================
def determine_unlocked_levels(
    difficulty_progress: Dict[str, Dict]
) -> Dict:
    """
    Determines which difficulty levels are unlocked.

    Input:
    - difficulty_progress from analytics_engine

    Output:
    - unlocked_levels
    - certification_ready flag
    """

    if not difficulty_progress:
        return {
            "unlocked_levels": ["beginner"],
            "certification_ready": False,
            "status": "insufficient_data"
        }

    unlocked = ["beginner"]

    if difficulty_progress.get("beginner", {}).get("post_accuracy", 0) >= 80:
        unlocked.append("intermediate")

    if difficulty_progress.get("intermediate", {}).get("post_accuracy", 0) >= 80:
        unlocked.append("advanced")

    certification_ready = (
        difficulty_progress.get("advanced", {}).get("post_accuracy", 0) >= 80
    )

    return {
        "unlocked_levels": unlocked,
        "certification_ready": certification_ready,
        "status": "ok"
    }
