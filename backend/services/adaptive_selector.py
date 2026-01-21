from typing import Dict, List

# ============================================================
# CONFIGURATION
# ============================================================

WEAK_MASTERY_THRESHOLD = 0.6
STRONG_MASTERY_THRESHOLD = 0.8


# ============================================================
# ADAPTIVE CONCEPT SELECTION ENGINE
# ============================================================

def select_concepts_for_next_quiz(
    concept_mastery: Dict[str, float],
    max_concepts: int = 8
) -> Dict:
    """
    Selects concepts adaptively for the next quiz.

    Strategy:
    - Weak concepts first
    - Then medium
    - Strong concepts last (or excluded)
    """

    weak = []
    medium = []
    strong = []

    for concept, mastery in concept_mastery.items():
        if mastery < WEAK_MASTERY_THRESHOLD:
            weak.append(concept)
        elif mastery < STRONG_MASTERY_THRESHOLD:
            medium.append(concept)
        else:
            strong.append(concept)

    # Deterministic ordering
    weak.sort()
    medium.sort()
    strong.sort()

    selected = []

    # 1️⃣ Always prioritize weak concepts
    for c in weak:
        if len(selected) < max_concepts:
            selected.append(c)

    # 2️⃣ Then medium mastery concepts
    for c in medium:
        if len(selected) < max_concepts:
            selected.append(c)

    # 3️⃣ Strong concepts only if needed
    for c in strong:
        if len(selected) < max_concepts:
            selected.append(c)

    return {
        "priority_concepts": selected,
        "weak_concepts": weak,
        "medium_concepts": medium,
        "strong_concepts": strong,
        "selection_strategy": "weak-first-deterministic"
    }
