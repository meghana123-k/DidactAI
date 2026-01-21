from typing import Dict, List

# ============================================================
# CONFIG
# ============================================================
DIFFICULTY_ORDER = ["beginner", "intermediate", "advanced"]

UNLOCK_RULES = {
    "beginner": {
        "min_accuracy": 60,
        "max_weak_concepts": 999  # no restriction
    },
    "intermediate": {
        "min_accuracy": 65,
        "max_weak_concepts": 2
    },
    "advanced": {
        "min_accuracy": 70,
        "max_weak_concepts": 0
    }
}

WEAK_CONCEPT_THRESHOLD = 40  # %

# ============================================================
# CORE LOGIC
# ============================================================
def determine_next_difficulty(
    analytics: Dict
) -> Dict:
    """
    Determines which difficulty level the user can access next.

    Input:
    - analytics output from analytics_engine

    Output:
    - progression decision
    """

    difficulty_stats = analytics["difficulty_analysis"]
    concept_stats = analytics["concept_analysis"]

    # Count weak concepts
    weak_concepts = [
        c for c, v in concept_stats.items()
        if v["accuracy"] < WEAK_CONCEPT_THRESHOLD
    ]

    unlocked = []
    blocked_reason = None

    for level in DIFFICULTY_ORDER:
        level_accuracy = difficulty_stats.get(level, {}).get("accuracy", 0)
        rules = UNLOCK_RULES[level]

        if level_accuracy < rules["min_accuracy"]:
            blocked_reason = (
                f"{level} accuracy {level_accuracy}% "
                f"is below required {rules['min_accuracy']}%"
            )
            break

        if len(weak_concepts) > rules["max_weak_concepts"]:
            blocked_reason = (
                f"Too many weak concepts ({len(weak_concepts)}) "
                f"for {level} level"
            )
            break

        unlocked.append(level)

    return {
        "unlocked_levels": unlocked,
        "next_level": _next_level(unlocked),
        "weak_concepts": weak_concepts,
        "blocked_reason": blocked_reason
    }


def _next_level(unlocked: List[str]) -> str:
    if not unlocked:
        return "beginner"

    last = unlocked[-1]
    idx = DIFFICULTY_ORDER.index(last)

    if idx + 1 < len(DIFFICULTY_ORDER):
        return DIFFICULTY_ORDER[idx + 1]

    return "certificate"
